import os
from cohere.embed import Embed

def asset_metadata_embedding(text):
    api_key = os.getenv('COHERE_API_KEY')
    embed = Embed(api_key=api_key)
    embedding = embed.embed(text)
    print(embedding)
    return embedding

if __name__ == '__main__':\n    asset_metadata_embedding('This is a sample text to embed.')