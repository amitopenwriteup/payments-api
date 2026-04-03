"""
AI Code Review Gate — Part 2
Calls the Anthropic API to perform semantic security review on a PR diff.
Exits 1 (blocking merge) when overall severity is HIGH.
"""
import anthropic
import json
import os
import sys

SYSTEM_PROMPT = """You are a senior security engineer reviewing a Python code diff
for a payments API. Your job is to identify security vulnerabilities and logic errors
in the changed code only — do not comment on unchanged context lines.

Evaluate the diff for:
- SQL injection via string formatting or concatenation in queries
- Hardcoded credentials, API keys, or secrets
- Missing authentication or authorisation checks on endpoints
- Unvalidated user input passed to exec, eval, subprocess, or file operations
- Insecure direct object references (IDOR)
- Missing input length or type validation

Respond with a single JSON object. No preamble, no markdown fences.
Schema:
{
  "severity": "LOW | MEDIUM | HIGH",
  "summary": "one sentence description of the overall change",
  "findings": [
    {
      "severity": "LOW | MEDIUM | HIGH",
      "line_hint": "approximate file:line if identifiable",
      "description": "what the issue is",
      "recommendation": "how to fix it"
    }
  ]
}

If there are no issues, return severity LOW with an empty findings array."""


def main() -> None:
    diff_path = "/tmp/pr_diff.txt"

    try:
        with open(diff_path) as f:
            diff = f.read()
    except FileNotFoundError:
        print("No diff file found — skipping review.")
        sys.exit(0)

    if not diff.strip():
        print("Empty diff — no Python files changed.")
        sys.exit(0)

    # Truncate very large diffs to stay within context limits
    if len(diff) > 12_000:
        diff = diff[:12_000] + "\n\n[diff truncated for review]"

    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Review this diff:\n\n{diff}"}],
    )

    raw = response.content[0].text.strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        print(f"Warning: LLM returned non-JSON response:\n{raw}")
        sys.exit(0)

    # Build PR comment body
    lines = [
        "## AI Code Review",
        f"**Overall severity:** `{result['severity']}`",
        f"**Summary:** {result['summary']}",
        "",
    ]

    if result.get("findings"):
        lines.append("### Findings\n")
        for i, finding in enumerate(result["findings"], 1):
            lines.append(f"**{i}. [{finding['severity']}]** {finding['description']}")
            if finding.get("line_hint"):
                lines.append(f"  - Location: `{finding['line_hint']}`")
            lines.append(f"  - Recommendation: {finding['recommendation']}")
            lines.append("")
    else:
        lines.append("✅ No security issues found.")

    summary = "\n".join(lines)

    with open("/tmp/review_summary.txt", "w") as f:
        f.write(summary)

    print(summary)

    # Emit GitHub Actions annotations
    for finding in result.get("findings", []):
        level = "error" if finding["severity"] == "HIGH" else "warning"
        print(f"::{level}::{finding['description']}")

    # Block merge on HIGH severity
    if result["severity"] == "HIGH":
        print("\n::error::AI review found HIGH severity issues. Merge is blocked.")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
