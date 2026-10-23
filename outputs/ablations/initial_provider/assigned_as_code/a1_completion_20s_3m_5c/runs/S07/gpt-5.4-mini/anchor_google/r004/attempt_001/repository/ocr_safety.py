import google.generativeai as genai


def ocr_safety(payload, config=None):
    config = config or {}
    genai.configure(api_key=config["api_key"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        f"Assess the following OCR text for unsafe content and respond with a concise JSON object: {payload['text']}"
    )
    return {"result": response.text}
