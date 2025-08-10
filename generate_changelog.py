import subprocess
import re
from datetime import datetime

# --------------------------
GITHUB_REPO = "XJTU-Qian-Xuesen-Class/XJTU-QXS" 
SITE_DOMAIN = "https://github.com/XJTU-Qian-Xuesen-Class/XJTU-QXZ"  

def get_git_log():
    """获取Git提交记录"""
    result = subprocess.run(
        ["git", "log", "--pretty=format:%H|%ad|%s", "--date=iso"],
        capture_output=True,
        text=True,
    )
    return result.stdout.splitlines()

def parse_commit(line):
    """解析每条提交记录"""
    sha, date_str, msg = line.split("|", 2)
    date = datetime.fromisoformat(date_str)
    
    # 提取PR链接（格式：#pr123）
    pr_match = re.search(r"#pr(\d+)", msg)
    pr_url = f"https://github.com/{GITHUB_REPO}/pull/{pr_match.group(1)}" if pr_match else ""
    
    # 提取课程页面链接（格式：课程名:路径）
    course_match = re.search(r"课程名:([^#]+)", msg)
    course_url = f"{SITE_DOMAIN}/courses/{course_match.group(1)}" if course_match else ""
    
    return {
        "sha": sha,
        "date": date.strftime("%Y-%m-%d"),
        "msg": msg,
        "pr_url": pr_url,
        "course_url": course_url,
        "is_archived": date < datetime(2025, 7, 20),
    }

def generate_markdown(commits):
    """生成更新日志的Markdown内容"""
    changelog = [
        "# 更新日志",
        "\n## 说明",
        "- 本页自动同步Git提交记录，按年份分组",
        "- 点击commit哈希可查看GitHub详情",
        "- 含「课程名:xxx」的提交可跳转对应页面\n"
    ]
    
    # 按年份分组
    year_groups = {}
    for commit in commits:
        year = commit["date"][:4]
        if year not in year_groups:
            year_groups[year] = []
        year_groups[year].append(commit)
    
    # 按年份倒序添加内容
    for year in sorted(year_groups.keys(), reverse=True):
        changelog.append(f"### {year} 年")
        for commit in year_groups[year]:
            sha_short = commit["sha"][:7]
            sha_url = f"https://github.com/{GITHUB_REPO}/commit/{commit['sha']}"
            
            changelog.append(f"\n#### {commit['date']}")
            changelog.append(f"- **提交**: [{sha_short}]({sha_url})")
            changelog.append(f"- **内容**: {commit['msg']}")
            
            if commit["pr_url"]:
                changelog.append(f"  - PR: [{commit['pr_url'].split('/')[-1]}]({commit['pr_url']})")
            if commit["course_url"]:
                changelog.append(f"  - 相关页面: [{commit['course_url'].split('/')[-1]}]({commit['course_url']})")
            if commit["is_archived"]:
                changelog.append(f"  - 提示: 该内容已存档")
    
    return "\n".join(changelog)

if __name__ == "__main__":
    try:
        commits = [parse_commit(line) for line in get_git_log()]
        markdown = generate_markdown(commits)
        with open("docs/changelog.md", "w", encoding="utf-8") as f:
            f.write(markdown)
        print("更新日志生成成功: docs/changelog.md")
    except Exception as e:
        print(f"生成失败: {e}")