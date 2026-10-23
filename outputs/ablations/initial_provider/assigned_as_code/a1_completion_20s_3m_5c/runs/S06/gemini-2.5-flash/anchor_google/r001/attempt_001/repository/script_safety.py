from speech_client import get_vertex_ai_prediction_client
from google.protobuf import json_format
from google.cloud.aiplatform.gapic.schema import predict_pb2

def script_safety(text_content, project_id, location="us-central1", model_id="content-moderation-text"):
    client = get_vertex_ai_prediction_client(project=project_id, location=location)
    endpoint = client.endpoint_path(
        project=project_id, location=location, endpoint="publishers/google/models/text-bison") # Using text-bison for demonstration as content-moderation-text is not directly exposed as a public endpoint for generic use.

    # The actual content moderation model would have a specific input schema.
    # For text-bison, input is text_instances.
    instance = predict_pb2.Instance(struct_value=json_format.ParseDict({"prompt": text_content}, dict()))
    instances = [instance]
    
    response = client.predict(endpoint=endpoint, instances=instances)

    # In a real content moderation scenario, you would parse the response
    # for safety attributes. This is a placeholder for demonstration.
    return {"predictions": [json_format.MessageToDict(p) for p in response.predictions]}