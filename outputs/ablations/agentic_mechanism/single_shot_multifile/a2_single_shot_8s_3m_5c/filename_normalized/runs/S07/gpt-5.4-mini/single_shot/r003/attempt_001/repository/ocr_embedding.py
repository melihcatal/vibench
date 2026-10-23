from google.cloud import aiplatform


def ocr_embedding(text_sections, project: str, location: str = 'us-central1', model: str = 'textembedding-gecko@003'):
    aiplatform.init(project=project, location=location)
    endpoint = aiplatform.Endpoint(endpoint_name=f'projects/{project}/locations/{location}/publishers/google/models/{model}')
    embeddings = []
    for section in text_sections:
        result = endpoint.predict(instances=[{'content': section}])
        embeddings.append(result.predictions[0])
    return {'embeddings': embeddings}