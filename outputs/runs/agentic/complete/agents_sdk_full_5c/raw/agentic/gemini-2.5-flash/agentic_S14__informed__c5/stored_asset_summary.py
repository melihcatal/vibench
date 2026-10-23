import os
import json
from storage_client import get_bedrock_runtime_client

def summarize_stored_asset_content(text_content: str, max_tokens: int = 512) -> str | None:
    bedrock_runtime_client = get_bedrock_runtime_client()
    try:
        # Using Amazon Titan Text Express v1 for summarization
        # Model ID: amazon.titan-text-express-v1 or amazon.titan-text-lite-v1
        model_id = "amazon.titan-text-express-v1"

        prompt = f"Summarize the following text:

{text_content}

Summary:"

        body = json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": max_tokens,
                "temperature": 0.7,
                "topP": 0.9
            }
        })

        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept='application/json',
            contentType='application/json'
        )

        response_body = json.loads(response.get('body').read())
        summary = response_body.get('results')[0].get('outputText')
        print(f"Content summarized using Amazon Titan Text Express v1 successfully.")
        return summary
    except Exception as e:
        print(f"Error summarizing content with Amazon Bedrock: {e}")
        return None
