from flask import Flask
import os

app = Flask(__name__)

@app.get("/healthz")
def health():
    return "ok", 200

@app.get("/")
def home():
    return "backend ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
