import hmac, hashlib, base64, json

key_b64 = "bWluaGEtd2hhbmUtc2VjcmV0YQo="
body = "{}"

digest = hmac.new(
    base64.b64decode(key_b64),
    body.encode(),
    hashlib.sha256
).digest()

signature = base64.b64encode(digest).decode()

print("X-Signature:", signature)
