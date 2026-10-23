from google.cloud import generativeai


def archive_summary(payload, config=None):
    config = config or {}
    model = generativeai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(payload["text"])
    return {"status": "COMPLETED", "summary": response.text}
