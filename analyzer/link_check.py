import re

def check_links(body_text):
    findings = []

    # Find all links in the email body
    links = re.findall(r'https?://[^\s]+', body_text)

    suspicious_patterns = [".ru", "verify", "-login", "secure-", "account-"]

    for link in links:
        for pattern in suspicious_patterns:
            if pattern in link.lower():
                findings.append({
                    "check": "Suspicious Link",
                    "detail": "Suspicious link found: " + link,
                    "weight": 2
                })
                break

    return findings
