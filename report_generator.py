
import os
from datetime import datetime


def generate_report(findings, email_file):
    total_weight = sum(item["weight"] for item in findings)
    total_findings = len(findings)

    if total_weight >= 4:
        verdict = "LIKELY PHISHING"
        overall_severity = "High"
    elif total_weight >= 1:
        verdict = "SUSPICIOUS - Review Needed"
        overall_severity = "Medium"
    else:
        verdict = "NO PHISHING INDICATORS DETECTED"
        overall_severity = "Low"

    lines = []
    lines.append("=" * 50)
    lines.append("Email analyzed: " + email_file)
    lines.append("Scan time: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    lines.append("Verdict: " + verdict)
    lines.append("Overall Severity: " + overall_severity)
    lines.append("Weighted risk score: " + str(total_weight))
    lines.append("Total findings: " + str(total_findings))
    lines.append("=" * 50)

    for item in findings:
        lines.append("- " + item["check"] + ": " + item["detail"])

    report_text = "\n".join(lines)

    print(report_text)

    email_name = os.path.splitext(os.path.basename(email_file))[0]
    report_path = os.path.join("reports", email_name + "_report.txt")

    os.makedirs("reports", exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print("\nReport saved to:", report_path)

    return verdict
