from amazoncomprehend import ComprehendClient


def message_safety(payload, config=None):
    config = config or {}
    client = ComprehendClient()
    text = payload.get("text", "")
    response = client.detect_dominant_language(Text=text)
    languages = response.get("Languages", [])
    return {"safe": bool(text), "languages": languages, "provider": "amazon-comprehend", "region": config.get("region")}
