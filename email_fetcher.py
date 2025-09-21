import imaplib, email
from scanner import scan_message
import time, os, uuid

def drop_email_to_folder(subject, body):
    folder = "watch_folder"
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Safe filename
    safe_subject = "".join(c for c in subject if c.isalnum() or c in (" ", "_")).strip()
    safe_subject = f"{safe_subject}_{uuid.uuid4().hex}.txt"

    file_path = os.path.join(folder, safe_subject)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(body)

    print(f"📥 Dropped email to folder: {safe_subject}")
    return file_path

def fetch_emails():
    print("📡 Checking for new emails...")
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login("cyberguardianemailfetcher2025@gmail.com", "isef vnzo tyvn euee")
        mail.select('inbox')

        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()
        print(f"📬 Found {len(email_ids)} unseen emails")

        for num in email_ids:
            status, data = mail.fetch(num, '(RFC822)')
            if status != 'OK':
                print("❌ Could not fetch email")
                continue

            msg = email.message_from_bytes(data[0][1])
            subject = msg['subject'] or "No Subject"
            sender = msg['from'] or "Unknown Sender"

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain" and part.get_payload(decode=True):
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode(errors="ignore")

            print(f"📧 Scanning email from {sender} | Subject: {subject}")
            scan_message(body, source=f"email : {subject}")

            file_path = drop_email_to_folder(subject, body)
            print(f"📁 Saved to: {os.path.abspath(file_path)}")

        mail.logout()
    except Exception as e:
        print(f"❌ Error fetching emails: {e}")

def start_email_fetcher():
    print("📡 Email fetcher started")
    while True:
        fetch_emails()
        time.sleep(60)  # check every 1 min

if __name__ == "__main__":
    start_email_fetcher()
