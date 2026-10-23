import boto3
import json
import os


def stored_asset_summary(payload, config=None):
    config = config or {}
    bedrock_runtime_client = boto3.client("bedrock-runtime", region_name=config.get("region") or os.environ.get("AWS_REGION"))
    text_to_summarize = payload["text"]

    # Using Anthropic Claude for summarization
    # The exact model ID might vary, using a common one for demonstration
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    prompt = f"Human: Summarize the following text:\n\n<text>\n{text_to_summarize}\n</text>\n\nAssistant:"

    body = json.dumps({"prompt": prompt, "max_tokens_to_sample": 500, "temperature": 0.5})

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())
    summary = response_body.get("completion", "No summary generated.")

    return {"original_text": text_to_summarize, "summary": summary}
