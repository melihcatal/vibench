from typing import Dict, Any

from observability_client import get_vertex_ai_text_client
from google.cloud.aiplatform_v1beta1.types import content as gapic_content_types
from google.protobuf import json_format

def metric_annotation_safety(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, bool]:
    config = config or {}
    client = get_vertex_ai_text_client(config["gcp_project_id"], config["gcp_region"])

    # For safety checking, we generally send content to a specific endpoint or use a model tuned for safety.
    # The actual implementation for safety might involve calling a specific safety API or a model with safety features.
    # This is a conceptual example using a general text model for demonstration.
    # In a real-world scenario, you'd integrate with a dedicated safety API or a fine-tuned model.

    # Construct the request for a general text model to check content safety (conceptual)
    # Note: This is a simplified representation. Actual safety API calls would differ.
    # A more robust solution would use Google Cloud's Safety API or a specific model for content moderation.
    instance = json_format.ParseDict({"prompt": payload["text_to_check"]}, gapic_content_types.TextContent())

    # This part is highly conceptual. A real safety check would involve a dedicated API/model.
    # Here, we are simulating a response based on keywords. DO NOT use this for production.
    is_safe = "unsafe" not in payload["text_to_check"].lower() and \
              "badword" not in payload["text_to_check"].lower()
    
    # If using a specific Vertex AI safety model, the call might look like this:
    # response = client.predict(endpoint="projects/YOUR_PROJECT/locations/YOUR_REGION/endpoints/YOUR_SAFETY_ENDPOINT", instances=[instance])

    return {"is_safe": is_safe}
