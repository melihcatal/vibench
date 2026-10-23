def normalize_text_response(response):
    if isinstance(response, dict):
        if "text" in response:
            return {"text": response["text"]}
        if "output" in response and isinstance(response["output"], dict):
            message = response["output"].get("message", {})
            content = message.get("content", [])
            text = "".join(block.get("text", "") for block in content if isinstance(block, dict))
            return {"text": text}
    return {"text": str(response)}


def build_user_payload(text, locale=None):
    payload = {"text": text}
    if locale:
        payload["locale"] = locale
    return payload
