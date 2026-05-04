import os
import re

import psycopg2
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-fallback-key")

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost/soonforward")


def get_db():
    return psycopg2.connect(DATABASE_URL)


@app.route("/")
def index():
    return render_template("index.html")


EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


@app.route("/submit", methods=["POST"])
def submit():
    email = request.form.get("email", "").strip().lower()

    if not email or not EMAIL_RE.match(email) or len(email) > 254:
        return redirect(url_for("index"))

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO emails (email_address) VALUES (%s)", (email,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("success"))
    except psycopg2.errors.UniqueViolation:
        return redirect(url_for("already_registered"))
    except Exception:
        return redirect(url_for("index"))


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/already-registered")
def already_registered():
    return render_template("already-registered.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(port=port, debug=True)
