import argparse
from email import message_from_file
from analyzer.urgency_check import check_urgency
from analyzer.sender_check import check_sender
from analyzer.link_check import check_links
from analyzer.reply_to_check import check_reply_to
from report_generator import generate_report

parser = argparse.ArgumentParser()
parser.add_argument("--email", required=True, help="Path to .eml file")
args = parser.parse_args()

with open(args.email) as f:
    msg = message_from_file(f)

from_address = msg.get("From", "")
reply_to_address = msg.get("Reply-To", "")
subject = msg.get("Subject", "")
body = ""

if msg.is_multipart():
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload()
else:
    body = msg.get_payload()

full_text = subject + " " + body

all_findings = []
all_findings += check_urgency(full_text)
all_findings += check_sender(from_address)
all_findings += check_links(body)
all_findings += check_reply_to(from_address, reply_to_address)

generate_report(all_findings, args.email)
