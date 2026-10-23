import openai

OPENAI_API_KEY = "your-openai-api-key"

client = openai.Client(api_key=OPENAI_API_KEY)


def caption_embedding(text):
    response = client.embeddings.create(input=text, model="text-embedding-ada-002")
    return response.data[0].embedding
