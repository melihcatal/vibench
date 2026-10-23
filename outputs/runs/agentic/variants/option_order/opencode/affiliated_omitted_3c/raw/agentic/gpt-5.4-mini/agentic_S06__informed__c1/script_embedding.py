from google import genai


def embed_script(text: str, api_key: str) -> list[float]:
    client = genai.Client(api_key=api_key)
    result = client.models.embed_content(
        model="models/text-embedding-004", contents=text
    )
    return result.embeddings[0].values
