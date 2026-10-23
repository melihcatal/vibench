import json

from safety_client import bedrock_runtime_client, load_model_id


DEFAULT_MODEL_ID = "amazon.titan-text-express-v1"


def appeal_translate(text: str, target_language: str) -> str:
    client = bedrock_runtime_client()
    model_id = load_model_id(DEFAULT_MODEL_ID)
    prompt = {"inputText": f"Translate to {target_language}: {text}", "textGenerationConfig": {"maxTokenCount": 128, "temperature": 0.0}}
    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(prompt).encode("utf-8"),
    )
    raw = json.loads(response["body"].read().decode("utf-8"))
    return str(raw.get("translation", raw.get("outputText", "")))
