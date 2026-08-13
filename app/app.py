import os
import psycopg2
from flask import Flask, render_template_string

app = Flask(__name__)

# ดึงค่าจาก ConfigMap และ Secret
DB_HOST = os.getenv("DB_HOST", "postgres-service")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secretpassword")
APP_ENV = os.getenv("APP_ENV", "production")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Python Fullstack K8s Demo</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f6f9; text-align: center; padding-top: 50px; }
        .card { background: white; width: 400px; margin: auto; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .status { color: green; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🚀 Python Full-Stack App</h2>
        <p>Environment: <strong>{{ env }}</strong></p>
        <p>Database Connection: <span class="status">{{ db_status }}</span></p>
        <p>Served by Pod: <strong>{{ hostname }}</strong></p>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    hostname = os.getenv("HOSTNAME", "unknown-pod")
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        conn.close()
        db_status = "Connected Successfully! 🎉"
    except Exception as e:
        db_status = f"Failed ({e})"

    return render_template_string(HTML_TEMPLATE, env=APP_ENV, db_status=db_status, hostname=hostname)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
