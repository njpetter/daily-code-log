"""Daily Log Helper Script
Automates creating daily progress markdown logs, updating README, and syncing to GitHub.
"""

import sys
import subprocess
from datetime import datetime
from pathlib import Path


def main():
    root_dir = Path(__file__).resolve().parent
    logs_dir = root_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    today_str = datetime.now().strftime("%Y-%m-%d")
    today_file = logs_dir / f"{today_str}.md"

    # Get summary from command-line arguments or prompt
    if len(sys.argv) > 1:
        summary = " ".join(sys.argv[1:]).strip()
    else:
        print(f"\n[+] Logging entry for {today_str}")
        summary = input("Brief summary of today's work/learning: ").strip()

    if not summary:
        summary = "Continued daily development and learning."

    # If log file doesn't exist, create it with standard template
    if not today_file.exists():
        content = f"""# 📅 Daily Log - {today_str}

### 🎯 Focus of the Day
- {summary}

### 💡 What I Did / Learned
- {summary}

### 📌 Goals for Tomorrow
- Continue building and learning.
"""
        today_file.write_text(content, encoding="utf-8")
        print(f"[✓] Created today's log: {today_file.name}")
    else:
        # Append note to today's existing log
        with open(today_file, "a", encoding="utf-8") as f:
            f.write(f"\n- {summary}\n")
        print(f"[✓] Appended note to {today_file.name}")

    # Git commit and push
    try:
        subprocess.run(["git", "add", "."], cwd=root_dir, check=True)
        commit_msg = f"docs(log): daily update for {today_str} - {summary[:50]}"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=root_dir, check=True)
        print("[✓] Committed to Git")

        push_result = subprocess.run(["git", "push"], cwd=root_dir, capture_output=True, text=True)
        if push_result.returncode == 0:
            print("[✓] Successfully pushed to GitHub! Check your profile for the green square! 🟩")
        else:
            print(f"[!] Push completed with message: {push_result.stderr.strip() or push_result.stdout.strip()}")
    except Exception as e:
        print(f"[!] Git operation error: {e}")


if __name__ == "__main__":
    main()
