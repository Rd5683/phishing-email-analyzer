import re

# Trusted real domains we check lookalikes against
KNOWN_BRANDS = {
    "paypal": "paypal.com",
    "amazon": "amazon.com",
    "google": "google.com",
    "microsoft": "microsoft.com",
    "apple": "apple.com",
    "netflix": "netflix.com",
    "facebook": "facebook.com",
    "instagram": "instagram.com",
    "linkedin": "linkedin.com",
    "sbi": "sbi.co.in",
    "hdfc": "hdfcbank.com",
    "icici": "icicibank.com",
    "axis bank": "axisbank.com",
    "kotak": "kotak.com",
    "pnb": "pnbindia.in",
    "paytm": "paytm.com",
    "phonepe": "phonepe.com",
    "googlepay": "pay.google.com",
    "razorpay": "razorpay.com",
    "flipkart": "flipkart.com",
    "myntra": "myntra.com",
    "swiggy": "swiggy.com",
    "zomato": "zomato.com",
    "ola": "olacabs.com",
    "irctc": "irctc.co.in",
    "income tax": "incometax.gov.in",
    "aadhaar": "uidai.gov.in",
    "jio": "jio.com",
    "airtel": "airtel.in"
}

def extract_domain(from_address):
    # Pull out just the actual email address part, e.g. from
    # "PayPal Security <security@paypa1-verify.com>" -> "security@paypa1-verify.com"
    match = re.search(r'<(.+?)>', from_address)
    if match:
        email_part = match.group(1)
    else:
        email_part = from_address.strip()

    # Now split on "@" to get just the domain
    if "@" in email_part:
        domain = email_part.split("@")[-1].lower().strip()
        return domain
    return ""

def is_domain_match(actual_domain, trusted_domain):
    # Exact match, OR a real subdomain of the trusted domain
    # e.g. "mail.paypal.com" is fine, but "paypal.com.attacker.com" is NOT
    if actual_domain == trusted_domain:
        return True
    if actual_domain.endswith("." + trusted_domain):
        return True
    return False

def check_sender(from_address):
    findings = []
    from_lower = from_address.lower()
    actual_domain = extract_domain(from_address)

    for brand, real_domain in KNOWN_BRANDS.items():
        if brand in from_lower:
            if not is_domain_match(actual_domain, real_domain):
                findings.append({
                    "check": "Sender Domain",
                    "detail": "Email mentions '" + brand + "' but actual sending domain is '" + actual_domain + "', not " + real_domain + " (full address: " + from_address + ")",
                    "weight": 2
                })

    return findings
