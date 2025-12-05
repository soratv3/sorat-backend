from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/healthz")
def healthz():
    return "ok", 200

@app.route("/gateway", methods=["POST"])
def gateway():
    body = request.json or {}
    return jsonify({
        "status": "received",
        "body": body
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
