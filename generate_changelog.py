import subprocess
import re
from datetime import datetime, timezone  # 新增 timezone 导入，解决时区比较问题

# --------------------------
# 替换为你的实际仓库信息
GITHUB_REPO = "XJTU-Qian-Xuesen-Class/XJTU-QXS"  
SITE_DOMAIN = "https://github.com/XJTU-Qian-Xuesen-Class/XJTU-QXZ"  
# --------------------------

def get_git_log():
    """获取Git提交记录（按时间倒序）"""
    result = subprocess.run(
        ["git", "log", "--pretty=format:%H|%ad|%s", "--date=iso"],
        capture_output=True,
        text=True,
    )
    return result.stdout.splitlines()

def parse_commit(line):
    """解析每条提交记录，处理时区问题"""
    sha, date_str, msg = line.split("|", 2)
    # 解析提交时间（含时区信息，offset-aware类型）
    date = datetime.fromisoformat(date_str)
    
    # 提取PR链接（格式：#pr123）
    pr_match = re.search(r"#pr(\d+)", msg)
    pr_url = f"https://github.com/{GITHUB_REPO}/pull/{pr_match.group(1)}" if pr_match else ""
    
    # 提取课程页面链接（格式：课程名:路径）
    course_match = re.search(r"课程名:([^#]+)", msg)
    course_url = f"{SITE_DOMAIN}/courses/{course_match.group(1)}" if course_match else ""
    
    # 关键修复：给截止日期添加UTC时区（与提交时间保持一致的offset-aware类型）
    archive_cutoff = datetime(2025, 7, 20, tzinfo=timezone.utc)
    
    return {
        "sha": sha,
        "date": date.strftime("%Y-%m-%d"),  # 格式化显示日期
        "msg": msg,
        "pr_url": pr_url,
        "course_url": course_url,
        "is_archived": date < archive_cutoff  # 现在可正常比较
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
    
    # 按年份分组提交记录
    year_groups = {}
    for commit in commits:
        year = commit["date"][:4]  # 从日期中提取年份（如"2024-05-10" → "2024"）
        if year not in year_groups:
            year_groups[year] = []
        year_groups[year].append(commit)
    
    # 按年份倒序添加内容（最新的年份在最前面）
    for year in sorted(year_groups.keys(), reverse=True):
        changelog.append(f"### {year} 年")
        for commit in year_groups[year]:
            sha_short = commit["sha"][:7]  # 只显示前7位哈希（简洁）
            sha_url = f"https://github.com/{GITHUB_REPO}/commit/{commit['sha']}"
            
            # 添加日期和提交信息
            changelog.append(f"\n#### {commit['date']}")
            changelog.append(f"- **提交**: [{sha_short}]({sha_url})")
            changelog.append(f"- **内容**: {commit['msg']}")
            
            # 附加PR链接（如果有）
            if commit["pr_url"]:
                changelog.append(f"  - PR: [{commit['pr_url'].split('/')[-1]}]({commit['pr_url']})")
            
            # 附加课程页面链接（如果有）
            if commit["course_url"]:
                changelog.append(f"  - 相关页面: [{commit['course_url'].split('/')[-1]}]({commit['course_url']})")
            
            # 显示存档提示（如果是2025.7.20之前的提交）
            if commit["is_archived"]:
                changelog.append(f"  - 提示: 该内容已存档")
    
    return "\n".join(changelog)

if __name__ == "__main__":
    try:
        # 获取并解析所有提交记录
        commits = [parse_commit(line) for line in get_git_log()]
        # 生成Markdown内容
        markdown = generate_markdown(commits)
        # 写入docs目录（让MkDocs能识别）
        with open("docs/changelog.md", "w", encoding="utf-8") as f:
            f.write(markdown)
        print("更新日志生成成功: docs/changelog.md")
    except Exception as e:
        print(f"生成失败: {e}")