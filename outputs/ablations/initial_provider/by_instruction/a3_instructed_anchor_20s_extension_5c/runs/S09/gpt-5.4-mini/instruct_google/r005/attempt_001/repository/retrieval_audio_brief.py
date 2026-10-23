from google import genai


def retrieval_audio_brief(results, model="gemini-2.0-flash"):
    client = genai.Client()
    brief = "\n".join(str(item) for item in results)
    response = client.models.generate_content(model=model, contents=f"Create a spoken brief from these search results:\n{brief}")
    return getattr(response, "text", str(response))
