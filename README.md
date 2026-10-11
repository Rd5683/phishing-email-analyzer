# Phishing Email Analyzer

A Python tool that analyzes `.eml` email files and detects common phishing red flags across four independent checks: urgency language, sender domain impersonation indicators, suspicious links, and Reply-To mismatches.

## Overview

Phishing remains one of the most common attack vectors used to compromise individuals and organizations. This tool automates the detection of common phishing indicators found in email files, producing a scored verdict and a saved report for each analysis — similar in concept to how real-world email security filters combine multiple signals rather than relying on a single check.

## How It Works

The tool checks four categories of red flags:

1. **Urgency Language** — scans the email body/subject for pressure phrases commonly used in phishing (e.g. "verify immediately," "act now," "suspended," "24 hours").

2. **Sender Domain Check** — compares the sender's claimed brand identity (e.g. "SBI," "PayPal," "Amazon") against a list of known real domains, flagging text-level mismatches that suggest impersonation. The sender's actual domain is properly extracted and compared using exact-match or valid-subdomain logic — not simple substring matching. This means a genuine subdomain like `mail.paypal.com` is correctly treated as valid, while a lookalike trick such as `paypal.com.attacker-evil.com` (where the real registered domain is actually `attacker-evil.com`) is correctly flagged instead of slipping through. **This check inspects the From header text only — it does not perform real sender authentication.** Verifying that an email genuinely originated from a claimed domain requires SPF, DKIM, and DMARC validation, which this tool does not implement.

3. **Suspicious Links** — extracts all links in the email body and flags ones matching configured risk patterns (certain TLD patterns associated with elevated phishing use, or keywords like "verify," "secure-", "account-", "-login"). A matching pattern is a configured indicator for review, not proof of malicious intent — a top-level domain alone is never evidence of phishing on its own.

4. **Reply-To Mismatch** — compares the "From" address domain against the "Reply-To" address domain (if present). A mismatch is a common phishing technique where the visible sender looks legitimate, but replies are silently redirected to the attacker's real inbox. Note: this signal is not definitive on its own — legitimate mailing lists and some third-party support systems can also produce a genuine From/Reply-To mismatch, so it is treated as one contributing indicator, not standalone proof.

Each detected finding is weighted, and the total score determines the final verdict:
- **LIKELY PHISHING** (score 4 or higher) — Overall Severity: High
- **SUSPICIOUS - Review Needed** (score 1 to 3) — Overall Severity: Medium
- **NO PHISHING INDICATORS DETECTED** (score 0) — Overall Severity: Low

## Tools and Technologies
- Python 3
- Python's built-in `email` library (for parsing `.eml` files)
- Python's built-in `re` library (for pattern matching and domain extraction)
- No external dependencies required

## Project Structure

```
Phishing-Email-Analyzer/
├── main.py                      → entry point, run with --email flag
├── report_generator.py          → builds verdict, severity, prints and saves report
├── analyzer/
│   ├── urgency_check.py         → detects pressure/urgency language
│   ├── sender_check.py          → detects sender domain impersonation indicators
│   ├── link_check.py            → detects suspicious links
│   └── reply_to_check.py        → detects From vs Reply-To domain mismatch
├── samples/                     → test .eml files
├── reports/                     → generated scan reports (.txt)
└── screenshots/                 → evidence of tool in action
```

## Usage

```bash
python3 main.py --email samples/your_email.eml
```

## Test Results

| Sample | Description | Verdict | Red Flags |
|---|---|---|---|
| phishing_sample1.eml | Fake PayPal account suspension email | LIKELY PHISHING | 10 |
| phishing_sample2.eml | Fake SBI KYC verification email | LIKELY PHISHING | 9 |
| phishing_sample3_bypass.eml | Domain lookalike bypass attempt (`paypal.com.attacker-evil.com`) | LIKELY PHISHING | 4 |
| phishing_sample4_replyto.eml | Legitimate-looking sender with mismatched Reply-To domain | SUSPICIOUS - Review Needed | 1 |
| normal_sample1.eml | Legitimate-style Amazon shipping notification | NO PHISHING INDICATORS DETECTED | 0 |

The tool detected the configured phishing indicators in all four test phishing scenarios, including a deliberate sender-domain bypass attempt. The included legitimate-style sample produced no findings. **These results apply only to the supplied test cases and do not represent real-world detection accuracy** — they demonstrate that the implemented logic functions correctly, not that the tool catches all phishing emails or guarantees zero false positives in general use.

## Development Notes: Fixing a Real Detection Bypass

During testing, an initial version of the sender domain check used simple substring matching (`if "paypal.com" in from_address`). This was found to be bypassable: an address like `security@paypal.com.attacker-evil.com` contains the text "paypal.com" and would incorrectly pass as legitimate.

The check was rewritten to properly extract the actual sending domain from the address and compare it using exact-match or valid-subdomain logic instead of substring containment. `phishing_sample3_bypass.eml` was created specifically to test and confirm this fix.

## Known Limitations
- Sender domain checking relies on a predefined list of known brands and inspects header text only — it is not a substitute for real sender authentication (SPF/DKIM/DMARC). A production-grade tool would also use broader lookalike-domain detection (e.g. Levenshtein distance / fuzzy string matching) to catch impersonation of any organization, not just listed ones — this is noted here as a deliberate scope decision, not an oversight.
- This tool analyzes static `.eml` files with plain-text bodies; it does not currently decode HTML-only or alternate MIME-encoded email bodies.
- Link analysis is pattern-based (keyword/TLD matching) and treats results as indicators for review, not confirmed proof of malicious intent.
- The Reply-To check can produce false positives for legitimate mailing lists or third-party support/ticketing systems that intentionally route replies to a different domain.
- Designed for educational and portfolio purposes, not production email security deployment.

## Disclaimer

This project was built for educational purposes as part of a cybersecurity portfolio. All test email samples are either self-created fictional examples or do not contain any real personal or sensitive information.
