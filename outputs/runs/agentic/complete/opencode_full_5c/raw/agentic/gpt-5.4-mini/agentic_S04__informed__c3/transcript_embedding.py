from openai import OpenAI


def transcript_embedding(segments):
    client = OpenAI()
    texts = [
        segment.get("text", "") if isinstance(segment, dict) else str(segment)
        for segment in segments
    ]
    result = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [item.embedding for item in result.data]
