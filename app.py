import os

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


@app.route("/submit", methods=["POST"])
def submit():
    email = request.form.get("email", "").strip().lower()

    if not email or "@" not in email:
        return redirect(url_for("invalid"))

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO emails (email) VALUES (%s)", (email,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("success"))
    except psycopg2.errors.UniqueViolation:
        return redirect(url_for("duplicate"))
    except Exception:
        return redirect(url_for("error"))


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/duplicate")
def duplicate():
    return render_template("duplicate.html")


@app.route("/invalid")
def invalid():
    return render_template("invalid.html")


@app.route("/error")
def error():
    return render_template("error.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
