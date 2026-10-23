import json

from speech_client import SpeechClient
from speech_models import SummarizeRequest


def archive_summary(request: SummarizeRequest, config=None) -> dict:
    config = config or {}
    client = SpeechClient(region_name=config.get("region")).get_bedrock_runtime_client()

    prompt = f"Human: Summarize the following transcript:

{request.transcript_text}

Assistant:"

    body = json.dumps({"prompt": prompt, "max_tokens_to_sample": request.max_tokens, "temperature": 0.1})

    response = client.invoke_model(
        body=body,
        modelId=request.model_id, # e.g., "anthropic.claude-v2"
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())
    summary = response_body.get("completion")

    return {"summary": summary}
