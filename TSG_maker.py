import requests
import os
import argparse
from pathlib import Path
import openai

# OpenAI API 키 가져오기
client = openai.OpenAI(api_key="user-key")

def analyze_issue_text(text):
    prompt = f"""
아래는 GitHub 이슈 본문입니다. 이 텍스트를 읽고 아래 항목을 분리해서 한국어로 정리해 주세요:

1. 문제 현상:
2. 원인:
3. 해결 방법:

--- 본문 시작 ---
{text}
--- 본문 끝 ---
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ OpenAI 분석 실패: {e}")
        return "문제 현상: 분석 실패\n원인: 분석 실패\n해결 방법: 분석 실패"

# 이슈 마크다운 포맷 구성
def format_issue_markdown(issue):
    title = issue.get("title", "제목 없음")
    body_raw = issue.get("body")
    body = body_raw.strip() if body_raw else ""
    url = issue.get("html_url")

    summary = analyze_issue_text(body)

    return f"""### 🔧 {title}

{summary}

[GitHub 이슈 보기]({url})

"""

# 이미 저장된 이슈 URL 수집
def get_existing_issue_urls(filepath):
    if not filepath.exists():
        return set()
    with filepath.open(encoding="utf-8") as f:
        lines = f.readlines()
    return {line.strip().split("(")[-1].rstrip(")\n") for line in lines if line.startswith("[GitHub 이슈 보기]")}

# Markdown 파일에 이슈 추가
def append_issues_to_md(issues, md_path, existing_urls):
    new_entries = [format_issue_markdown(issue) for issue in issues if issue.get("html_url") not in existing_urls]
    if not new_entries:
        print("🟢 추가할 새로운 이슈가 없습니다.")
        return
    with open(md_path, "a", encoding="utf-8") as f:
        for entry in new_entries:
            f.write(entry + "\n")
    print(f"✅ {len(new_entries)}개의 이슈를 추가했습니다: {md_path.name}")

# GitHub API에서 Closed 이슈 가져오기
def get_closed_issues(owner, repo, token):
    issues = []
    page = 1
    headers = {"Authorization": f"token {token}"}
    while True:
        params = {"state": "closed", "per_page": 100, "page": page}
        response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/issues", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"GitHub API Error: {response.status_code} - {response.text}")
        data = response.json()
        if not data:
            break
        for issue in data:
            if "pull_request" not in issue:  # PR은 제외
                issues.append(issue)
        page += 1
    return issues

# 메인 실행 함수
def main():
    parser = argparse.ArgumentParser(description="GitHub Closed 이슈 기반 트러블슈팅 Markdown 생성기")
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

    append_issues_to_md(issues, md_path, existing_urls)

if __name__ == "__main__":
    main()
