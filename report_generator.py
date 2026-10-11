import os
from datetime import datetime

def generate_report(findings, email_file):
    total_weight = sum(item["weight"] for item in findings)

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
    lines.append("Total red flags: " + str(len(findings)))
    lines.append("=" * 50)

    for item in findings:
        lines.append("- " + item["check"] + ": " + item["detail"])

    report_text = "\n".join(lines)

    print(report_text)

    email_name = os.path.basename(email_file).replace(".eml", "")
    report_path = "reports/" + email_name + "_report.txt"

    with open(report_path, "w") as f:
        f.write(report_text)

    print("\nReport saved to:", report_path)

    return verdict
