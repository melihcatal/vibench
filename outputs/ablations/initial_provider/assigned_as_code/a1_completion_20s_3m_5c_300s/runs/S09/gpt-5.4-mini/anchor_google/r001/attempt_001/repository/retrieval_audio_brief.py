from google import genai


def retrieval_audio_brief(payload, config=None):
    config = config or {}
    client = genai.Client(api_key=config.get("api_key"))
    response = client.models.generate_content(model="gemini-2.0-flash", contents=str(payload.get("results", [])) + " Provide a short spoken brief.")
    return {"brief": response.text}
