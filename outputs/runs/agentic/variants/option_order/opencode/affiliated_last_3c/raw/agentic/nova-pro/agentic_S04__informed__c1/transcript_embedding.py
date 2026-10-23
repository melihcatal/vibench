from openai import Embedding


def transcript_embedding(transcript):
    api_key = os.getenv("OPENAI_API_KEY")
    embedding = Embedding(api_key=api_key)
    vector = embedding.create(input=transcript)
    return vector["data"][0]["embedding"]
