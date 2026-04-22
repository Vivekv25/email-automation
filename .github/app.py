# app.py

from flask import Flask, render_template, request, redirect
import os
import pandas as pd
import subprocess

app = Flask(__name__)

# -----------------------------
# FOLDERS
# -----------------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------------
# LOGIN PAGE
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email and password:
            return redirect("/dashboard")

    return render_template("login.html")


# -----------------------------
# DASHBOARD
# -----------------------------
@app.route("/dashboard")
def dashboard():

    leads = []
    filename = "No file uploaded"

    files = os.listdir(UPLOAD_FOLDER)

    if files:
        files.sort()
        filename = files[-1]

        filepath = os.path.join(UPLOAD_FOLDER, filename)

        try:
            df = pd.read_csv(filepath)

            for _, row in df.iterrows():

                email = str(row.iloc[0]).strip()

                if "@" in email:
                    name = email.split("@")[0].replace(".", " ").title()
                else:
                    name = "Unknown"

                status = "Pending"

                if len(row) > 1:
                    status = str(row.iloc[1]).strip().title()

                leads.append({
                    "email": email,
                    "name": name,
                    "status": status
                })

        except Exception as e:
            print(e)

    # -----------------------------
    # LIVE STATS
    # -----------------------------
    total = len(leads)

    sent = len([x for x in leads if x["status"] == "Sent"])

    failed = len([x for x in leads if x["status"] == "Failed"])

    pending = len([x for x in leads if x["status"] == "Pending"])

    rate = round((sent / total) * 100) if total > 0 else 0

    return render_template(
        "dashboard.html",
        leads=leads,
        filename=filename,
        total=total,
        sent=sent,
        failed=failed,
        pending=pending,
        rate=rate,
        message=""
    )


# -----------------------------
# CSV UPLOAD + RUN CAMPAIGN
# -----------------------------
@app.route("/upload", methods=["POST"])
def upload():

    file = request.files.get("csv_file")

    if file and file.filename != "":

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        subprocess.Popen(

    ["python3", "src/clean_and_gen_call_script.py", filepath]

)

    return redirect("/dashboard")


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8000)