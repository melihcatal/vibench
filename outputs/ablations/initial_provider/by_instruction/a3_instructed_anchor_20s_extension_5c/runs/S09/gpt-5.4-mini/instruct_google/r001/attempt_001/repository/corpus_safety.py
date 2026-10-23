from google import genai


def corpus_safety(texts):
    client = genai.Client(api_key="")
    prompt = f"Check these texts for unsafe content before embedding: {texts}"
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text
