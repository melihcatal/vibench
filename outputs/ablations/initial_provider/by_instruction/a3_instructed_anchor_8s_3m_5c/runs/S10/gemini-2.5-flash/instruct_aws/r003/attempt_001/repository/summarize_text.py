import boto3
import os

def summarize_text(text: str) -> str:
    client = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    
    # Using Claude 3 Sonnet for summarization
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    prompt = f"""
    Human: Summarize the following text:
    <text>
    {text}
    </text>
    Assistant:
    """
    
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ]
    }
    
    response = client.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )
    
    response_body = json.loads(response.get("body").read())
    return response_body["content"][0]["text"]

if __name__ == '__main__':
    import json
    # Example usage:
    long_text = "Your very long text here that needs summarization. This could be multiple paragraphs, an article, or any extensive content you want to condense into a shorter form."
    summary = summarize_text(long_text)
    print("Summary:", summary)
