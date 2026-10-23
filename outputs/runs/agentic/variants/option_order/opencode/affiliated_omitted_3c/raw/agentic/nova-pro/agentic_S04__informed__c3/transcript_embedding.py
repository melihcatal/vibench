from openai import OpenAI


def transcript_embedding(transcript):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=transcript, model="text-embedding-ada-002"
    )
    return response.data[0].embedding
