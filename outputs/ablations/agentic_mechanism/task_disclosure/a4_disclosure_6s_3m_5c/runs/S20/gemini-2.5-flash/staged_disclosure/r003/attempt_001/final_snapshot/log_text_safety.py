import os
from google.cloud import automl_v1beta1 as automl

def check_safety(log_message: str) -> dict:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    model_id = os.environ.get("GOOGLE_CLOUD_AUTOML_MODEL_ID")

    if not project_id or not model_id:
        return {"error": "Google Cloud Project ID or AutoML Model ID not set in environment variables."}

    client = automl.PredictionServiceClient()

    # Get the full path of the model.
    model_full_id = client.model_path(project_id, "us-central1", model_id)

    text_snippet = automl.TextSnippet(content=log_message, mime_type="text/plain")
    payload = automl.ExamplePayload(text_snippet=text_snippet)

    try:
        response = client.predict(name=model_full_id, payload=payload)
        safety_scores = {}
        for annotation_payload in response.payload:
            safety_scores[annotation_payload.display_name] = annotation_payload.classification.score
        return {"safety_scores": safety_scores}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage (requires GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_AUTOML_MODEL_ID env vars)
    message_to_check = "This is a test log message with potentially unsafe content."
    result = check_safety(message_to_check)
    print(result)
