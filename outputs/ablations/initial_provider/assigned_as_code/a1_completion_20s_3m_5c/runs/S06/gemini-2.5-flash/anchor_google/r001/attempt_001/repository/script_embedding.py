from speech_client import get_vertex_ai_prediction_client
from google.protobuf import json_format
from google.cloud.aiplatform.gapic.schema import predict_pb2

def script_embedding(text_content, project_id, location="us-central1", model_id="text-embedding-garden"):
    client = get_vertex_ai_prediction_client(project=project_id, location=location)
    endpoint = client.endpoint_path(
        project=project_id, location=location, endpoint=f"publishers/google/models/{model_id}")

    # The input for text embeddings is typically a list of text instances.
    instance = predict_pb2.Instance(struct_value=json_format.ParseDict({"content": text_content}, dict()))
    instances = [instance]
    
    response = client.predict(endpoint=endpoint, instances=instances)

    embeddings = []
    for prediction in response.predictions:
        # Assuming the embedding is directly in a 'embeddings' field of the prediction
        if "embeddings" in prediction and "values" in prediction["embeddings"]:
            embeddings.append(list(prediction["embeddings"]["values"]))
    
    return {"embeddings": embeddings}