import requests
import os
import argparse
from pathlib import Path
import openai

# OpenAI API 키 가져오기
client = openai.OpenAI(api_key="user-key")

# 이슈 내용 요약 (필요에 따라 OpenAI 사용)
def analyze_issue_text(text):
    prompt = f"""
Below is the body of a GitHub issue. The purpose is to analyze the problem phenomenon, cause, and solution from this content and create a troubleshooting guide that can be provided to customers experiencing the same issue. Please read this text and organize it only in English as follows:

1. Problem Phenomenon (The issue):
2. Cause (The cause of the issue):
3. Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):

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
    # AI 분석이 필요하면 아래 줄의 주석을 해제
    summary = analyze_issue_text(summary)

    return f"""### 🔧 {title}

{summary}

[View GitHub Issue]({url})

"""


# 기존 이슈 URL 수집
def get_existing_issue_urls(filepath):
    if not filepath.exists():
        return set()
    with filepath.open(encoding="utf-8") as f:
        lines = f.readlines()
    return {line.strip().split("(")[-1].rstrip(")\n") for line in lines if line.startswith("[GitHub 이슈 보기]")}


# Markdown 파일에 이슈 추가
def append_issues_to_md(issues, md_path, existing_urls, owner, repo, token):
    new_entries = []
    for issue in issues:
        url = issue.get("html_url")
        if url not in existing_urls:
            issue_number = issue.get("number")
            comments = get_issue_comments(owner, repo, issue_number, token)
            entry = format_issue_markdown(issue, comments)
            new_entries.append(entry)
    if not new_entries:
        print("🟢 추가할 새로운 이슈가 없습니다.")
        return
    with open(md_path, "a", encoding="utf-8") as f:
        for entry in new_entries:
            f.write(entry + "\n")
    print(f"✅ {len(new_entries)}개의 이슈를 추가했습니다: {md_path.name}")


# 메인 실행 함수
def main():
    parser = argparse.ArgumentParser(description="GitHub Closed 이슈 및 댓글 Markdown 생성기")
    parser.add_argument("token", help="GitHub Personal Access Token")
    parser.add_argument("owner", help="GitHub 저장소 소유자")
    parser.add_argument("repo", help="GitHub 저장소 이름")
    parser.add_argument("--output", default="troubleshooting_guide.md", help="출력할 Markdown 파일명")
    args = parser.parse_args()

    md_path = Path(args.output)
    existing_urls = get_existing_issue_urls(md_path)
    print("📥 기존 Markdown 파일에서 URL 수집 완료")

    issues = get_closed_issues(args.owner, args.repo, args.token)
    print(f"📦 총 {len(issues)}개의 Closed 이슈를 수집했습니다")

    append_issues_to_md(issues, md_path, existing_urls, args.owner, args.repo, args.token)

if __name__ == "__main__":
    main()
