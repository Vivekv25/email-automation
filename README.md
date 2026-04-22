# 🚀 Email Marketing AI Agent

An AI-powered system that reads user engagement data, generates personalized emails using AI, and sends them automatically.

---

## 📌 Overview

This project automates email marketing workflows:
- Collects user data from Google Sheets
- Analyzes engagement (email opens)
- Generates AI-based personalized emails
- Sends emails automatically using SMTP

---

## ⚡ Features

- AI-generated personalized emails  
- Dynamic tone based on engagement  
- Google Sheets integration  
- Automated email sending  
- Batch processing (anti-spam delay)  

---

## 🏗️ Project Structure

```
email-marketing-ai-agent/
│
├── src/
│   ├── helpers/
│   │   ├── config.py
│   │   ├── create_call_script.py
│   │   ├── utils.py
│   │
│   ├── clean_and_gen_call_script.py
│
├── requirements.txt
├── README.md
├── .gitignore
└── .env (ignored)
```

---

## 🛠️ Tech Stack

- Python  
- OpenRouter (DeepSeek AI)  
- Google Sheets API  
- Gmail SMTP  
- dotenv  

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/Vivekv25/email-marketing-ai-agent.git
cd email-marketing-ai-agent
```

---

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create `.env` file

```
OPENROUTER_API_KEY=your_api_key
SENDER_EMAIL=your_email@gmail.com
EMAIL_APP_PASSWORD=your_app_password
```

---

### 5. Add Google Credentials

Place your `credentials.json` inside:
```
src/credentials.json
```

---

## ▶️ Usage

```bash
PYTHONPATH=./src python3 src/clean_and_gen_call_script.py
```

---

## 🔄 How It Works

1. Fetch data from Google Sheets  
2. Check engagement (open rate)  
3. Generate AI email  
4. Send email via SMTP  
5. Update status  

---

## ⚠️ Security

- Never upload `.env`  
- Never upload `credentials.json`  
- Keep API keys private  

---