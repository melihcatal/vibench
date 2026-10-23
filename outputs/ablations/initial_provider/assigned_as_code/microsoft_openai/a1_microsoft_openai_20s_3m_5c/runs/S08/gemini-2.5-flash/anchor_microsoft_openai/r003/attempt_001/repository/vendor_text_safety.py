import os
from typing import Dict, Any
from google.cloud import aiplatform
from google.protobuf import json_format
from google.cloud.aiplatform.gapic.schema import predict_pb2


def moderate_vendor_text(vendor_text: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", config.get("project_id"))
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", config.get("location", "us-central1"))
    publisher = "google"
    model_id = "gemini-1.0-pro"

    if not all([project_id, location]):
        raise ValueError("Missing GOOGLE_CLOUD_PROJECT_ID or GOOGLE_CLOUD_LOCATION environment variables or config values.")

    aiplatform.init(project=project_id, location=location)

    # Using Gemini Pro for safety attribute analysis
    prompt = f"""Analyze the following vendor note for safety attributes such as toxicity, harassment, hate speech, dangerous content, and sexual content. Provide a safety score for each category and an overall assessment.\n\nVendor Note:\n{vendor_text}"""

    try:
        response = aiplatform.predict.PredictionClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}).predict(
            endpoint=aiplatform.helpers.to_resource_name(project_id, location, publisher, model_id),
            instances=[predict_pb2.Instance(struct_value=json_format.ParseDict({"prompt": prompt}, predict_pb2.Instance().struct_value)).struct_value],
        )
        safety_analysis = response.predictions[0].struct_value["content"]
        return {"safety_analysis": safety_analysis}
    except Exception as e:
        return {"error": f"Failed to moderate vendor text: {str(e)}"}
