import random
import time
import os
import requests
import smtplib
from email.mime.text import MIMEText

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
load_dotenv()

from helpers.config import (
    email_google_sheet,
    call_script_google_sheet,
    CLIENT_ID,
    CLIENT_SECRET,
    REFRESH_TOKEN,
    ZOHO_API_BASE_URL,
    TOKEN_URL
)

# ================= AI EMAIL GENERATION =================

def generate_ai_email(email, open_amount):
    try:
        api_key = os.getenv("OPENROUTER_API_KEY")

        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        name = email.split("@")[0].split(".")[0].capitalize()

        style = random.choice([
            "casual and friendly",
            "professional and concise",
            "enthusiastic and energetic",
            "curious and exploratory"
        ])

        prompt = f"""
Write ONE short personalized follow-up email.

Context:
- Name: {name}
- Engagement score: {open_amount}
- Style: {style}

Rules:
- Start with: Hi {name},
- Keep it 3–4 lines ONLY
- Use natural human tone
- Mention engagement subtly
- End with a question
- End naturally WITHOUT any closing like "Cheers" or "Best"

STRICTLY:
- No "Best", "Regards", or signature
- No placeholders like [Your Name]
- No explanations
- Only ONE email

Return ONLY the email.
"""

        data = {
            "model": "deepseek/deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if "choices" in result:
            content = result["choices"][0]["message"]["content"]

            # cleanup unwanted AI output
            content = content.split("Note:")[0]
            content = content.split("Best,")[0]
            content = content.split("Regards,")[0]
            content = content.split("Cheers,")[0]
            content = content.split("[Your Name]")[0]
            content = content.strip()       

            return content
        else:
            print("AI error:", result)
            return f"Hi {name}, just checking in!"

    except Exception as e:
        print("AI failed:", e)
        return f"Hi {email}, just checking in!"


# ================= EMAIL SENDER =================

def send_email(receiver_email, body):
    sender_email = os.getenv("SENDER_EMAIL")
    app_password = os.getenv("EMAIL_APP_PASSWORD")

    name = receiver_email.split("@")[0].split(".")[0].capitalize()

    subject_options = [
        f"Quick thought, {name}",
        f"Following up, {name}",
        f"{name}, quick question",
        "Something you might find interesting"
    ]

    subject = random.choice(subject_options)

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print(f"[Agent] Email sent to {receiver_email}")
    except Exception as e:
        print(f"[Agent] Email failed: {e}")


# ================= GOOGLE SHEETS =================

def authorize_google_sheets():
    try:
        print("Authorizing Google Sheets...")
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            "src/credentials.json", scope
        )
        return gspread.authorize(credentials)
    except Exception as e:
        raise Exception(f"Error authorizing Google Sheets: {e}")


def upload_to_google_sheet(email, call_script, new_sheet_id):
    client = authorize_google_sheets()
    try:
        sheet = client.open_by_key(new_sheet_id).sheet1
        first_name, last_name = (email.split('@')[0].split('.') + [""])[:2]
        sheet.append_row([email, first_name, last_name, call_script])
        print(f"Uploaded to output sheet: {email}")
    except Exception as e:
        print(f"Upload error: {e}")


# ================= MAIN PROCESS =================

def process_email_tracking(sheet_id, new_sheet_id):
    print("Function started")

    try:
        client = authorize_google_sheets()
        sheet = client.open_by_key(sheet_id).sheet1
        rows = sheet.get_all_records()
        print("Rows fetched:", rows)
    except Exception as e:
        print("ERROR:", e)
        return

    count = 0
    MAX_EMAILS = 5

    for index, row in enumerate(rows):

        if count >= MAX_EMAILS:
            break

        try:
            email = row.get('Email_address')
            status = row.get('Status', 'pending')

            if status == 'done':
                continue

            open_amount = row.get('Open_Amount', '')
            open_amount = int(open_amount) if open_amount else 0

            print(f"[Agent] Processing {email} | opens: {open_amount}")

            if open_amount > 5:
                call_script = generate_ai_email(email, open_amount)

                print("\n===== EMAIL =====")
                print(email)
                print("\n===== CALL SCRIPT =====")
                print(call_script)

                upload_to_google_sheet(email, call_script, new_sheet_id)
                send_email(email, call_script)

                count += 1
                time.sleep(random.randint(2, 5))

                sheet.update_cell(index + 2, 3, "done")

        except Exception as e:
            print(f"Row error: {e}")


# ================= RUN =================

RUN_LOOP = False  # change to True for demo

if __name__ == "__main__":
    source_sheet_id = email_google_sheet
    destination_sheet_id = call_script_google_sheet

    if RUN_LOOP:
        print("Agent running...")
        while True:
            process_email_tracking(source_sheet_id, destination_sheet_id)
            time.sleep(10)
    else:
        print("Running once...")
        process_email_tracking(source_sheet_id, destination_sheet_id)


#to run this use : PYTHONPATH=./src python3 src/clean_and_gen_call_script.py