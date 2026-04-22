# Email Marketing AI Agent

AI-powered email outreach automation platform built using **Python**, **Flask**, and modern AI integration.  
This web application allows users to upload lead lists through CSV files, generate personalized outreach emails automatically, send campaigns, and monitor progress through a professional dashboard.

---

## Overview

Email Marketing AI Agent was built to automate cold and warm outreach workflows by combining lead management, AI-generated email writing, campaign execution, and real-time dashboard analytics into one system.

This project demonstrates practical skills in backend development, automation systems, API integration, frontend UI design, and workflow engineering.

---

## Features

### Lead Management
- Upload CSV files containing lead emails
- Automatic CSV parsing
- Name extraction from email addresses
- Lead table display inside dashboard

### AI Email Generation
- Personalized outreach emails using AI
- Human-like writing style
- Dynamic tone variations
- Follow-up focused messaging

### Campaign Automation
- Automated email sending through SMTP
- Batch lead processing
- Failed send handling
- Status updates after each email

### Dashboard Analytics
- Total leads count
- Emails sent count
- Pending leads count
- Open rate metric
- Progress bar tracking
- Auto-refresh updates

### Status Indicators
- Sent
- Pending
- Failed
- Opened

### UI / UX
- Login page
- Responsive dashboard
- Modern glassmorphism design
- Clean professional layout

---

## Screenshots

### Login Page
<img width="1706" height="904" alt="login" src="https://github.com/user-attachments/assets/689388ef-a148-4c4c-8b1e-09bd70ecdea7" />


### Dashboard

<img width="1703" height="905" alt="dashboard" src="https://github.com/user-attachments/assets/97ecd340-cef4-4ee6-b999-82519f5e428e" />



---

## Tech Stack

- Python
- Flask
- Pandas
- HTML5
- CSS3
- Jinja2
- SMTP
- Git
- GitHub

---

## Project Structure

```bash
email-marketing-ai-agent/
│── app.py
│── README.md
│── requirements.txt
│── .gitignore
│── .env.example
│
├── templates/
│   ├── login.html
│   └── dashboard.html
│
├── static/
│   ├── dashboard-bg.jpg
│   └── images.jpg
│
├── src/
│   ├── clean_and_gen_call_script.py
│   └── get_emails.py
│
├── uploads/
│
└── assets/
    ├── login.png
    └── dashboard.png
```
## Installation
```
# Clone repository
Environment Variables
git clone https://github.com/Vivekv25/email-automation.git

# Enter project folder
cd email-automation

# Install dependencies
pip install -r requirements.txt
```
## Environment Variables
- Create a .env file in the project root:
  ```
  OPENROUTER_API_KEY=your_key_here
  SENDER_EMAIL=your_email_here
  EMAIL_APP_PASSWORD=your_password_here
  ```
## Run Project
```
 python3 app.py
```
-Open Browser
```
http://127.0.0.1:8000
```
## CSV Sample Format
```
email,status

john@gmail.com,Pending

demo@gmail.com,Pending

client@gmail.com,Pending
```
## Workflow
```
1. Login to dashboard
2. Upload CSV leads file
3. System reads lead data
4. AI generates personalized emails
5. Emails are sent automatically
6. Dashboard updates statuses live
```








  

