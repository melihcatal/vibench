from google.cloud import discoveryengine_v1alpha as discoveryengine

def embed_caption(text):
    client = discoveryengine.DocumentServiceClient()
    document = discoveryengine.types.Document(content=text, mime_type='text/plain')
    response = client.embed_document(document)
    return response.embedding.values