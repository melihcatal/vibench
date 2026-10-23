import os
import openai

# Set up the API key
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"


# Function to embed text
def embed_text(text):
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return response["data"][0]["embedding"]
