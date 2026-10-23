from google import genai


def retrieval_audio_brief(results):
    client = genai.Client(api_key="")
    prompt = f"Create a spoken brief from these retrieved search results: {results}"
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text
