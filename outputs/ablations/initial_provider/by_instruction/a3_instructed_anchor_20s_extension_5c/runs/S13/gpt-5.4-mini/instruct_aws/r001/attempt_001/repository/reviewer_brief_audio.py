import json

from safety_client import bedrock_runtime_client, load_model_id


DEFAULT_MODEL_ID = "amazon.titan-text-express-v1"


def reviewer_brief_audio(brief_text: str) -> bytes:
    client = bedrock_runtime_client()
    model_id = load_model_id(DEFAULT_MODEL_ID)
    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps({"inputText": brief_text, "textGenerationConfig": {"maxTokenCount": 256, "temperature": 0.0}}).encode("utf-8"),
    )
    raw = json.loads(response["body"].read().decode("utf-8"))
    return str(raw.get("audio", raw.get("outputText", ""))).encode("utf-8")
