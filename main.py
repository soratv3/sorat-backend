from flask import Flask, request, jsonify
import hmac, hashlib, base64, json, os

app = Flask(__name__)

# Carrega o mapa de clientes HMAC do Render
hmacClientMap = json.loads(os.environ.get("GATEWAY_HMAC_CLIENT_MAP", "{}"))

def verify_hmac(body_raw, signature, client_id):
    if client_id not in hmacClientMap:
        return False

    # Decodifica chave Base64
    key = base64.b64decode(hmacClientMap[client_id])

    # Gera o digest HMAC SHA256
    digest = hmac.new(key, body_raw, hashlib.sha256).digest()

    # Converte digest para Base64
    expected = base64.b64encode(digest).decode()

    # Compara as assinaturas
    return hmac.compare_digest(expected, signature)


@app.route("/gateway", methods=["POST"])
def gateway():
    body_raw = request.data or b""  # garante bytes
    body_json = request.get_json(silent=True) or {}

    client_id = request.headers.get("X-Client-Id", "")
    signature = request.headers.get("X-Signature", "")

    if not client_id or not signature:
        return jsonify({"error": "missing headers"}), 400

    ok = verify_hmac(body_raw, signature, client_id)

    if not ok:
        return jsonify({"error": "invalid signature"}), 401

    return jsonify({"status": "ok", "received": body_json}), 200


@app.route("/healthz")
def healthz():
    return "ok", 200
