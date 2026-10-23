import os
import json
from storage_client import get_bedrock_runtime_client
from storage_models import SummaryResult

def summarize_stored_asset_content(text_content: str, max_tokens: int = 200):
    """
    Summarizes content extracted from a stored asset using Amazon Bedrock with an Anthropic Claude model.
    Note: Using Claude as an example, but other models (like Amazon Titan Text) can be used.
    """
    bedrock_runtime_client = get_bedrock_runtime_client()
    model_id = "anthropic.claude-instant-v1" # Example model, can be amazon.titan-text-express-v1 as well

    prompt = f"Human: Summarize the following text in a concise manner: {text_content}\n\nAssistant:"

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": max_tokens,
        "temperature": 0.7,
        "top_p": 0.9
    })

    try:
        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept='application/json',
            contentType='application/json'
        )
        response_body = json.loads(response.get('body').read())
        summary = response_body.get('completion')
        print(f"Summary (first 100 chars): {summary[:100]}...")
        return SummaryResult(source_text=text_content, summary=summary, model_id=model_id)
    except Exception as e:
        print(f"Error summarizing content with Amazon Bedrock: {e}")
        return None

# Example of identifiable signal: Amazon Bedrock Runtime is used via boto3 client `bedrock_runtime_client` and modelId `anthropic.claude-instant-v1`
