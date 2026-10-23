import boto3
import json
import os

def summarize_text_with_bedrock(text_content: str, max_tokens: int = 200):
    """
    Summarizes text content using Amazon Bedrock Runtime with a Titan model.
    """
    bedrock_runtime_client = boto3.client('bedrock-runtime')
    model_id = "amazon.titan-text-express-v1" # Or amazon.titan-text-lite-v1

    prompt = f"Summarize the following text:\n\n{text_content}"

    body = json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": max_tokens,
            "stopSequences": [],
            "temperature": 0.5,
            "topP": 0.9
        }
    })

    try:
        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )
        response_body = json.loads(response.get('body').read())
        summary = response_body['results'][0]['outputText']
        print(f"Generated summary: {summary.strip()}")
        return summary.strip()
    except Exception as e:
        print(f"Error summarizing text with Bedrock: {e}")
        return None

