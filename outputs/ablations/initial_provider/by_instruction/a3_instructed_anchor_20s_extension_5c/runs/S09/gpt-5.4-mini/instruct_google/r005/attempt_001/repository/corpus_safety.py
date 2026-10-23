from google import genai


def corpus_safety(texts, model="gemini-2.0-flash"):
    client = genai.Client()
    verdicts = []
    for text in texts:
        response = client.models.generate_content(model=model, contents=f"Assess safety for embedding: {text}")
        verdicts.append(getattr(response, "text", str(response)))
    return verdicts
