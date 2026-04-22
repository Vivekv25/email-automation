# src/clean_and_gen_call_script.py

import random
import os
import sys
import time
import requests
import smtplib
import pandas as pd

from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# AI EMAIL GENERATION
# ==========================================

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

        selected_angle = random.choice([
            "increasing qualified leads",
            "improving conversions",
            "saving time with automation",
            "customer retention",
            "stronger online visibility",
            "scaling outreach faster",
            "better response rates",
            "campaign performance growth",
            "qualified prospects",
            "brand awareness"
        ])

        prompt = f"""
You are writing a smart follow-up email to a warm lead.

Lead Info:
- Name: {name}
- Style: {style}
- Opportunity: {selected_angle}

Rules:
- Start with: Hi {name},
- 6 to 8 short lines only
- Natural human tone
- No robotic style
- No signature
- No Regards / Best / Cheers
- Create curiosity
- End with one question

Return only email body.
"""

        data = {
            "model": "deepseek/deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(url, headers=headers, json=data, timeout=60)
        result = response.json()

        if "choices" in result:
            content = result["choices"][0]["message"]["content"].strip()

            bad_words = [
                "Best,",
                "Regards,",
                "Cheers,",
                "[Your Name]",
                "Note:"
            ]

            for word in bad_words:
                content = content.split(word)[0]

            return content.strip()

        return f"Hi {name}, wanted to reconnect and share an idea that may help. Open to hearing it?"

    except Exception as e:
        print("AI Error:", e)
        return f"Hi {email}, wanted to reconnect and share an idea that may help. Interested?"


# ==========================================
# SEND EMAIL
# ==========================================

def send_email(receiver_email, body):
    sender_email = os.getenv("SENDER_EMAIL")
    app_password = os.getenv("EMAIL_APP_PASSWORD")

    if not sender_email or not app_password:
        print("Missing EMAIL credentials in .env")
        return False

    name = receiver_email.split("@")[0].split(".")[0].capitalize()

    subject = random.choice([
        f"Quick thought, {name}",
        f"{name}, quick question",
        f"Following up, {name}",
        "Something worth sharing"
    ])

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

        print("Email sent to:", receiver_email)
        return True

    except Exception as e:
        print("Email failed:", receiver_email, e)
        return False


# ==========================================
# PROCESS CSV FILE
# ==========================================

def process_csv(csv_file):

    try:
        df = pd.read_csv(csv_file)

        # Keep only first 2 columns
        df = df.iloc[:, :2]

        # Rename columns properly
        df.columns = ["email", "status"]

    except Exception as e:
        print("CSV Read Error:", e)
        return

    count = 0
    max_emails = 5

    for index, row in df.iterrows():

        if count >= max_emails:
            break

        try:
            email = str(row.iloc[0]).strip()

            if "@" not in email:
                continue

            print("Processing:", email)

            open_amount = 10

            body = generate_ai_email(email, open_amount)

            success = send_email(email, body)

            if success:
                df.at[index, "status"] = "Sent"
            else:
                df.at[index, "status"] = "Failed"

            count += 1

            time.sleep(random.randint(2, 5))

        except Exception as e:
            print("Row Error:", e)
            df.at[index, "status"] = "Failed"

    # Save updated CSV
    df.to_csv(csv_file, index=False)

    print("Campaign finished")


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    if len(sys.argv) > 1:

        csv_file = sys.argv[1]

        print("Running campaign using:", csv_file)

        process_csv(csv_file)

    else:
        print("No CSV file provided")