from google import genai


def output_embedding(text: str):
    client = genai.Client(api_key="")
    return client.models.embed_content(model="text-embedding-004", contents=text)
