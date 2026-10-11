# Words/phrases commonly used to create fake urgency in phishing emails
URGENCY_WORDS = [
    "urgent", "immediately", "act now", "suspended",
    "verify your account", "24 hours", "failure to act",
    "click here", "limited time", "act fast"
]

def check_urgency(body_text):
    findings = []
    text_lower = body_text.lower()

    for phrase in URGENCY_WORDS:
        if phrase in text_lower:
            findings.append({
                "check": "Urgency Language",
                "detail": "Found urgency phrase: '" + phrase + "'",
                "weight": 1
            })

    return findings
