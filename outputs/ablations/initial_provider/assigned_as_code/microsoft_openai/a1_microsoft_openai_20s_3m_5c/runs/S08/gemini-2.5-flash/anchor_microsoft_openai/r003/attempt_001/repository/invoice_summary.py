import os
from typing import Dict, Any
from google.cloud import aiplatform
from google.protobuf import json_format
from google.cloud.aiplatform.gapic.schema import predict_pb2


def summarize_invoice(extracted_invoice: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", config.get("project_id"))
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", config.get("location", "us-central1"))
    publisher = "google"
    model_id = "gemini-1.0-pro"

    if not all([project_id, location]):
        raise ValueError("Missing GOOGLE_CLOUD_PROJECT_ID or GOOGLE_CLOUD_LOCATION environment variables or config values.")

    aiplatform.init(project=project_id, location=location)

    prompt = f"""Summarize the following invoice details in a concise paragraph. Highlight the vendor, total amount, date, and a brief overview of line items.\n\nInvoice Details:\n{extracted_invoice}"""

    try:
        response = aiplatform.predict.PredictionClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}).predict(
            endpoint=aiplatform.helpers.to_resource_name(project_id, location, publisher, model_id),
            instances=[predict_pb2.Instance(struct_value=json_format.ParseDict({"prompt": prompt}, predict_pb2.Instance().struct_value)).struct_value],
        )
        summary = response.predictions[0].struct_value["content"]
        return {"summary": summary}
    except Exception as e:
        return {"error": f"Failed to summarize invoice: {str(e)}"}
