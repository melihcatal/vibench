import boto3
from security_client import resolve_secret_name


def rotation_summary() -> dict:
    client = boto3.client("bedrock-runtime")
    secret_id = resolve_secret_name("ROTATION_SECRET_ID", "app/rotating-secret")
    prompt = f"Summarize the rotation status for secret {secret_id} in one concise JSON object."
    body = {"inputText": prompt, "textGenerationConfig": {"maxTokenCount": 128, "temperature": 0}}
    response = client.invoke_model(modelId="amazon.nova-lite-v1:0", body=str(body).encode("utf-8"))
    return {"secret_id": secret_id, "response": response.get("body").read().decode("utf-8")}
