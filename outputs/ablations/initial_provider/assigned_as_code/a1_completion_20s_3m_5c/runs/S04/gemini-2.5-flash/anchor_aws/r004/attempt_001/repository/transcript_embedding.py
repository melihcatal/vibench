from openai import OpenAI


def transcript_embedding(text, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key"))
    
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding
