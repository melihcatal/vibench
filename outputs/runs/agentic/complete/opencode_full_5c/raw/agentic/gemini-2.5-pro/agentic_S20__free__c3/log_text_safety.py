from google.cloud import aiplatform
from google.protobuf import struct_pb2


def check_log_text_safety(
    log_message: str, project_id: str, location: str = "us-central1"
):
    """
    Checks log message for unsafe content using the Vertex AI Text Moderation API.
    """
    aiplatform.init(project=project_id, location=location)

    api_endpoint = f"{location}-aiplatform.googleapis.com"
    client_options = {"api_endpoint": api_endpoint}

    # The model name for text moderation
    model_name = "text-moderation@001"

    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

    instance = struct_pb2.Struct()
    instance.fields["content"].string_value = log_message

    instances = [instance]

    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_name}"

    response = client.predict(endpoint=endpoint, instances=instances)

    safety_ratings = {}
    for prediction in response.predictions:
        for category, severity in prediction.items():
            safety_ratings[category] = severity

    return safety_ratings


if __name__ == "__main__":
    import os

    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if project:
        unsafe_log = "User comment included a threat of violence."
        safety_check = check_log_text_safety(unsafe_log, project_id=project)
        print(f"Safety check for: '{unsafe_log}'")
        print(safety_check)

        safe_log = "User reported a bug in the checkout process."
        safety_check_safe = check_log_text_safety(safe_log, project_id=project)
        print(f"\nSafety check for: '{safe_log}'")
        print(safety_check_safe)
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable must be set.")
