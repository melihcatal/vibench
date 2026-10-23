import json
from storage_client import get_bedrock_client
from storage_models import SummaryResult


def summarize_text(text: str) -> SummaryResult | None:
    bedrock_client = get_bedrock_client()
    prompt = f"\n\nHuman: Please provide a concise summary of the following text:\n\n{text}\n\nAssistant:"
    body = json.dumps(
        {
            "prompt": prompt,
            "max_tokens_to_sample": 300,
            "temperature": 0.1,
            "top_p": 0.9,
        }
    )

    try:
        response = bedrock_client.invoke_model(
            body=body,
            modelId="anthropic.claude-v2",
            accept="application/json",
            contentType="application/json",
        )
        response_body = json.loads(response.get("body").read())
        summary = response_body.get("completion")
        return SummaryResult(summary=summary.strip())
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return None
