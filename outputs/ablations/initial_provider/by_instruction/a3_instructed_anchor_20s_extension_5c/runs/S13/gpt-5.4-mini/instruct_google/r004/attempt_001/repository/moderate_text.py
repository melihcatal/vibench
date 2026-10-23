import json
from urllib import request

from safety_client import load_safety_config, google_headers
from safety_models import SafetyDecision, normalize_text


def moderate_text(text: str) -> SafetyDecision:
    cfg = load_safety_config()
    prompt = normalize_text(text)
    body = {
        "contents": [{"parts": [{"text": f"Classify this text for safety issues and return JSON with allowed, category_scores, rationale: {prompt}"}]}],
        "generationConfig": {"temperature": 0, "responseMimeType": "application/json"},
    }
    url = f"{cfg.google_base_url}/v1beta/models/{cfg.google_model}:generateContent?key={cfg.google_api_key or ''}"
    req = request.Request(url, data=json.dumps(body).encode(), headers=google_headers(cfg.google_api_key), method="POST")
    with request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())
    text_out = data["candidates"][0]["content"]["parts"][0]["text"]
    parsed = json.loads(text_out)
    return SafetyDecision(allowed=bool(parsed.get("allowed")), category_scores=parsed.get("category_scores", {}), rationale=parsed.get("rationale", ""))
