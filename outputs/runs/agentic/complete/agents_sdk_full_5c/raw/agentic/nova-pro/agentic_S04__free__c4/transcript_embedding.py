from google.cloud import discoveryengine_v1alpha as discoveryengine

def transcript_embedding(transcript):
    client = discoveryengine.DocumentServiceClient()
    document = discoveryengine.Document(content=transcript)
    response = client.embed_document(request={'document': document})
    return response.embedding.values