from google import genai


def retrieval_audio_brief(payload, config=None):
    config = config or {}
    client = genai.Client(api_key=config.get("api_key"))
    response = client.models.generate_content(model="gemini-2.5-flash", contents=payload["retrieved_results"])
    return {"brief_text": response.text}
