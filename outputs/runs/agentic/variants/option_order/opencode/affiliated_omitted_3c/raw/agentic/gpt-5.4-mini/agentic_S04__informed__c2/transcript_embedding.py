import os
from cohere import ClientV2


def transcript_embedding(segments):
    client = ClientV2(api_key=os.environ["COHERE_API_KEY"])
    texts = [segment if isinstance(segment, str) else segment.get("text", "") for segment in segments]
    response = client.embed(model="embed-english-v3.0", texts=texts, input_type="search_document")
    return {"embeddings": response.embeddings.float}
