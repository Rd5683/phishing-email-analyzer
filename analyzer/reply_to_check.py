import re

def extract_domain(address):
    # Pull just the domain out of an email address string
    match = re.search(r'<(.+?)>', address)
    if match:
        email_part = match.group(1)
    else:
        email_part = address.strip()

    if "@" in email_part:
        return email_part.split("@")[-1].lower().strip()
    return ""

def check_reply_to(from_address, reply_to_address):
    findings = []

    # If there's no Reply-To header at all, nothing to check
    if not reply_to_address:
        return findings

    from_domain = extract_domain(from_address)
    reply_domain = extract_domain(reply_to_address)

    # If reply-to domain is different from the from domain, that's suspicious
    if reply_domain and from_domain and reply_domain != from_domain:
        findings.append({
            "check": "Reply-To Mismatch",
            "detail": "Email claims to be from '" + from_domain + "' but replies would go to a different domain: '" + reply_domain + "'",
            "weight": 2
        })

    return findings
