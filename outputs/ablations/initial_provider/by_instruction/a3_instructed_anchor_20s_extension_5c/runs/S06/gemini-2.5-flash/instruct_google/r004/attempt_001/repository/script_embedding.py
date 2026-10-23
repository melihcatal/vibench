from google.cloud import aiplatform

def get_script_embedding(project_id: str, location: str, text: str):
    aiplatform.init(project=project_id, location=location)

    # The model_id should correspond to a text embedding model, e.g., 'textembedding-gecko@001'
    model = aiplatform.get_model("textembedding-gecko@001")

    response = model.predict(instances=[{"content": text}])
    # Assuming the response contains an embedding for the input text
    if response.predictions and len(response.predictions) > 0:
        # The exact structure might vary, but typically embeddings are in a list
        return response.predictions[0]['embeddings']
    return None
