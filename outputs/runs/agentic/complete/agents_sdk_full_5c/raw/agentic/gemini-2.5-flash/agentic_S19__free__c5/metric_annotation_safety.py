from google.cloud.aiplatform_v1 import PredictionServiceClient
from google.cloud.aiplatform_v1.types import PredictRequest
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

def check_annotation_safety(project_id: str, location: str, annotation_text: str):
    api_endpoint = f"{location}-aiplatform.googleapis.com"
    client = PredictionServiceClient(client_options={"api_endpoint": api_endpoint})

    endpoint_name = client.endpoint_path(
        project=project_id, location=location, endpoint="content-safety-v1-endpoint" # Conceptual endpoint ID
    )

    instance = json_format.ParseDict({"content": annotation_text}, Value())
    instances = [instance]

    try:
        # This call is simulated for demonstration purposes. It will fail at runtime
        # without a real Vertex AI endpoint for content safety.
        response = client.predict(
            request=PredictRequest(
                endpoint=endpoint_name,
                instances=instances,
            )
        )
        # Simulate a safety check based on keywords for the purpose of this exercise.
        if "unsafe" in annotation_text.lower() or "harmful" in annotation_text.lower():
             return {"safety_check": "FLAGGED", "reason": "Simulated: potentially unsafe content detected"}
        return {"safety_check": "SAFE", "reason": "Simulated: no unsafe content detected"}

    except Exception as e:
        return {"safety_check": "ERROR", "reason": f"Vertex AI Content Safety API simulation error: {e}"}
