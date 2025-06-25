import requests
import os
import argparse
from pathlib import Path
import openai
import markdown2  # ✅ HTML 변환용
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pyperclip
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

# .env 파일 로딩
load_dotenv("my_key.env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
MAKER_EMAIL = os.getenv("MAKER_EMAIL")
MAKER_PASSWORD = os.getenv("MAKER_PASSWORD")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")
OUTPUT_NAME = os.getenv("OUTPUT_NAME")
TSG_FILE_NAME = os.getenv("TSG_FILE_NAME", "troubleshooting_guide.md")
TODO_FILE_NAME = os.getenv("TODO_FILE_NAME", "ToDolist.md")


def remove_bullet_and_numbering(text):
    cleaned_lines = []
    for line in text.splitlines():
        stripped = line.strip()
        # 1. 또는 - 또는 * 로 시작하는 줄 제거
        if re.match(r"^(\d+\.|- |\* )", stripped):
            # 숫자 글머리나 기호 제거
            cleaned_line = re.sub(r"^(\d+\.\s+|- |\* )", "", line)
            cleaned_lines.append(cleaned_line)
        else:
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

# ✅ 마크다운을 HTML로 변환
def markdown_to_html(md_text):
    return markdown2.markdown(md_text)

# 이슈 내용 요약 (필요에 따라 OpenAI 사용)
def analyze_issue_text(text):
    prompt = f"""
Below is the body of a GitHub issue. The purpose is to analyze the problem phenomenon, cause, and solution from this content and create a troubleshooting guide that can be provided to customers experiencing the same issue. Please read this text and organize it only in English as follows:

## Problem Phenomenon (The issue):
## Cause (The cause of the issue):
## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):

--- Start of Issue Content ---
{text}
--- End of Issue Content ---
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ OpenAI Analysis Failed: {e}")
        return "Problem: Analysis failed\nCause: Analysis failed\nSolution: Analysis failed"

def extract_todo_from_issue(text):
    prompt = f"""
Below is a GitHub issue discussion (including body and comments).
Your task is to determine whether there is any feature request or technical requirement that represents a new capability, significant functional enhancement, or integration demand which WIZnet (a network solution provider) could support or address.

Ignore minor code cleanups, bug fix suggestions, or cosmetic refactoring.

Focus only on substantive feature requests or technical needs (e.g., non-blocking APIs, new protocol support, architecture compatibility, etc.).

If such a request exists:

Extract the core feature request or technical suggestion in English (summarized).

Provide a brief background explanation of what this request implies or why it's needed.

If not, return "NONE".

--- GitHub Issue Content ---
{text}
--- End of Content ---
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ OpenAI ToDo 분석 실패: {e}")
        return "NONE"


# GitHub API로 Closed 이슈 가져오기
def get_closed_issues(owner, repo, token):
    issues = []
    page = 1
    headers = {"Authorization": f"token {token}"}
    while True:
        params = {"state": "closed", "per_page": 100, "page": page}
        response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/issues",
            headers=headers,
            params=params
        )
        if response.status_code != 200:
            raise Exception(f"GitHub API Error: {response.status_code} - {response.text}")
        data = response.json()
        if not data:
            break
        for issue in data:
            if "pull_request" not in issue:  # PR 제외
                issues.append(issue)
        page += 1
    return issues

def get_open_issues(owner, repo, token):
    issues = []
    page = 1
    headers = {"Authorization": f"token {token}"}
    while True:
        params = {"state": "open", "per_page": 100, "page": page}
        response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/issues",
            headers=headers,
            params=params
        )
        if response.status_code != 200:
            raise Exception(f"GitHub API Error (Open Issues): {response.status_code} - {response.text}")
        data = response.json()
        if not data:
            break
        for issue in data:
            if "pull_request" not in issue:  # PR 제외
                issues.append(issue)
        page += 1
    return issues

# 특정 이슈에 대한 댓글 가져오기
def get_issue_comments(owner, repo, issue_number, token):
    comments = []
    page = 1
    headers = {"Authorization": f"token {token}"}
    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
        params = {"per_page": 100, "page": page}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"GitHub API Error (Comments): {response.status_code} - {response.text}")
        data = response.json()
        if not data:
            break
        for comment in data:
            comments.append(comment.get("body", ""))
        page += 1
    return comments


# 마크다운 포맷
def format_issue_markdown(issue, comments=None):
    title = issue.get("title", "제목 없음")
    body_raw = issue.get("body", "")
    body = body_raw.strip().replace("''", "'")
    url = issue.get("html_url")

    comments_md = ""
    if comments:
        for idx, comment in enumerate(comments, 1):
            comments_md += f"\n**💬 Comment {idx}:**\n{comment}\n"

    summary = body + comments_md
    summary = analyze_issue_text(summary)

    md_result = f"""# [Title] {title}

{summary}

[View GitHub Issue]({url})

"""
    html_result = markdown_to_html(md_result)
    return md_result, html_result, title

# 기존 이슈 URL 수집
def get_existing_issue_urls(filepath):
    if not filepath.exists():
        return set()
    with filepath.open(encoding="utf-8") as f:
        lines = f.readlines()
    return {line.strip().split("(")[-1].rstrip(")\n") for line in lines if line.startswith("[GitHub 이슈 보기]")}

def get_existing_todo_urls(filepath):
    if not Path(filepath).exists():
        return set()
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    return set(re.findall(r"\[View Issue\]\((https://github\.com/.+?)\)", content))

def append_open_issues_to_todolist(issues, owner, repo, token, output_path="ToDolist.md"):
    existing_urls = get_existing_todo_urls(output_path)
    new_entries = []
    for issue in issues:
        issue_number = issue.get("number")
        issue_url = issue.get("html_url")

        if issue_url in existing_urls:
            continue  # 중복 방지

        title = issue.get("title")
        body = issue.get("body", "")
        comments = get_issue_comments(owner, repo, issue_number, token)
        full_text = f"{body}\n" + "\n".join(comments)
        
        summary = extract_todo_from_issue(full_text)
        if summary != "NONE":
            md = f"""### {title}

- **Suggestion**: {summary}  
- [View Issue]({issue_url})  

"""
            new_entries.append(md)

    if not new_entries:
        print("🟢 Open 이슈 중 대응할 항목이 없습니다.")
        return

    with open(output_path, "a", encoding="utf-8") as f:
        for entry in new_entries:
            f.write(entry + "\n")

    print(f"✅ {len(new_entries)}개 항목이 ToDolist.md에 추가되었습니다.")


def append_issues_to_md_and_upload(issues, md_path, existing_urls, owner, repo, token):
    new_entries = []
    for issue in issues:
        url = issue.get("html_url")
        if url not in existing_urls:
            issue_number = issue.get("number")
            comments = get_issue_comments(owner, repo, issue_number, token)
            md, html, title = format_issue_markdown(issue, comments)
            new_entries.append((md, html, title))

    if not new_entries:
        print("🟢 추가할 새로운 이슈가 없습니다.")
        return

    with open(md_path, "a", encoding="utf-8") as f:
        for md, html, title in new_entries:
            f.write(md + "\n")

    print(f"✅ {len(new_entries)}개의 이슈를 Markdown 저장했습니다.")

def input_text_with_send_keys(element, text, chunk_size=300):
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        element.send_keys(chunk)
        time.sleep(0.1)  # 너무 빠르면 누락될 수 있어 약간의 지연 추가


def paste_text_using_clipboard(element, text):
    pyperclip.copy(text)  # 텍스트를 클립보드에 복사
    element.click()       # 에디터 활성화
    time.sleep(0.5)
    element.send_keys(Keys.CONTROL, 'v')  # 붙여넣기 (Mac은 COMMAND로 변경)
    time.sleep(1)  # 붙여넣기 완료까지 대기

def upload_full_issue_list(repo_name, all_text):
    driver = webdriver.Chrome()
    driver.get("https://maker.wiznet.io/forum")
    driver.maximize_window()

    # 로그인
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "layLoginBtn"))).click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "loginFrm")))
    time.sleep(0.5)
    #driver.execute_script("""
    #    document.querySelector("input[name='email']").value = "{MAKER_EMAIL}";
    #    document.querySelector("input[name='pass']").value = "{MAKER_PASSWORD}";
    #""")
    driver.execute_script(f"""
        document.querySelector("input[name='email']").value = "{MAKER_EMAIL}";
        document.querySelector("input[name='pass']").value = "{MAKER_PASSWORD}";
    """)
    time.sleep(0.3)
    driver.find_element(By.CLASS_NAME, "loginBtn").click()
    print("✅ 로그인 완료")

    time.sleep(1)
    driver.get("https://maker.wiznet.io/forum/write")
    time.sleep(1)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn_addProject"))).click()
    time.sleep(1)

    # 제목 입력: <repo 이름> issue list
    driver.find_element(By.ID, "inputSubject").send_keys(f"{repo_name} issue list")
    time.sleep(1)

    driver.find_element(By.ID, "categoryTrigger").click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "#categorySelector button[data-idx='18']").click()
    time.sleep(1)

    # 본문 입력
    editor_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".ck-editor__main div[contenteditable='true']"))
    )
    driver.execute_script("arguments[0].focus();", editor_div)
    paste_text_using_clipboard(editor_div, all_text)

    time.sleep(3)

    # reCAPTCHA 수동 처리 안내
    iframe = driver.find_element(By.CSS_SELECTOR, "iframe[title*='reCAPTCHA']")
    driver.switch_to.frame(iframe)
    print("🛑 reCAPTCHA 수동 처리 필요")
    time.sleep(3)
    input("🛑 수동 인증 후 Enter 키를 눌러 게시 완료...")


# 메인 실행 함수
def main():
    parser = argparse.ArgumentParser(description="GitHub Closed 이슈 분석 + Maker 게시 자동화")
    parser.add_argument("--upload-only", action="store_true", help="기존 Markdown 파일 내용을 기반으로 Maker에만 업로드")
    parser.add_argument("--todo", action="store_true", help="Open 상태 이슈를 분석하여 ToDolist.md에 기록")
    args = parser.parse_args()

    # 명령어 모드 설정 (필요시)
    upload_only = False
    analyze_open = False

    # OpenAI 클라이언트 초기화
    global client
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    md_path = Path(TSG_FILE_NAME)

    if args.upload_only:
        if not md_path.exists():
            print(f"❌ Markdown 파일이 존재하지 않습니다: {args.output}")
            return

        print(f"📄 {TSG_FILE_NAME} 파일을 읽고 Maker에 이슈를 통합 게시합니다...")

        with md_path.open("r", encoding="utf-8") as f:
            contents = f.read()

        issue_blocks = contents.split("# [Title] ")[1:]
        merged_md = ""
        for block in issue_blocks:
            title_end = block.find("\n")
            title = block[:title_end].strip()
            md_text = "# [Title] " + block.strip()
            cleaned = remove_bullet_and_numbering(md_text)
            merged_md += cleaned + "\n\n"

        upload_full_issue_list(GITHUB_REPO, merged_md)
        print(f"✅ 저장소의 모든 이슈를 Maker 포럼에 업로드 완료.")
        return
    
    if args.todo:
        print("🧭 Open 이슈 중 요청사항 분석 중...")
        open_issues = get_open_issues(GITHUB_OWNER, GITHUB_REPO, GITHUB_TOKEN)
        append_open_issues_to_todolist(open_issues, GITHUB_OWNER, GITHUB_REPO, GITHUB_TOKEN, TODO_FILE_NAME)
        return

    # 기존 로직 (GitHub 이슈를 새로 불러오는 경우)
    existing_urls = get_existing_issue_urls(md_path)
    print("📥 기존 Markdown 파일에서 URL 수집 완료")

    issues = get_closed_issues(GITHUB_OWNER, GITHUB_REPO, GITHUB_TOKEN)
    print(f"📦 총 {len(issues)}개의 Closed 이슈를 수집했습니다")

    append_issues_to_md_and_upload(issues, md_path, existing_urls, GITHUB_OWNER, GITHUB_REPO, GITHUB_TOKEN)

    if not md_path.exists():
        print(f"❌ Markdown 파일이 존재하지 않습니다: {args.output}")
        return

    #print(f"📄 {args.output} 파일을 읽고 Maker에 이슈를 통합 게시합니다...")

    with md_path.open("r", encoding="utf-8") as f:
        contents = f.read()

    issue_blocks = contents.split("# [Title] ")[1:]
    merged_md = ""
    for block in issue_blocks:
        title_end = block.find("\n")
        title = block[:title_end].strip()
        md_text = "# [Title] " + block.strip()
        cleaned = remove_bullet_and_numbering(md_text)
        merged_md += cleaned + "\n\n"

    upload_full_issue_list(GITHUB_REPO, merged_md)
    print(f"✅ {GITHUB_REPO} 저장소의 모든 이슈를 Maker 포럼에 업로드 완료.")


if __name__ == "__main__":
    main()