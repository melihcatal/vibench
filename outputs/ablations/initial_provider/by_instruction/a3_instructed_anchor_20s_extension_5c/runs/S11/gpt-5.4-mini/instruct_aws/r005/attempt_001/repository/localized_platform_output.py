from model_client import bedrock_runtime_client, model_id
from model_models import json_body


def localized_platform_output(text: str, target_locale: str = "es"):
    client = bedrock_runtime_client()
    response = client.invoke_model(
        modelId=model_id(),
        body=json_body({"inputText": f"Translate to {target_locale}: {text}"}),
        contentType="application/json",
        accept="application/json",
    )
    return response
