from google.cloud import generativeai as genai


def meeting_summary(payload, config=None):
    config = config or {}
    genai.configure(api_key=config.get("api_key") or config.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    transcript = "\n".join(payload["chunks"])
    response = model.generate_content(f"Summarize this meeting transcript succinctly:\n{transcript}")
    return {"summary": response.text, "source": "google-generativeai", "model": "gemini-1.5-flash"}
