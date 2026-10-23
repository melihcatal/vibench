import boto3
import json
from typing import Generator

def stream_completion(prompt_text: str) -> Generator[str, None, None]:
    """
    Streams partial output tokens from AWS Bedrock using an LLM.
    """
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1"
    )

    prompt = f"""Human: {prompt_text}
Assistant:"""

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 500,
        "temperature": 0.7,
        "top_p": 0.9
    })

    model_id = "anthropic.claude-v2"
    content_type = "application/json"
    accept = "application/json"

    response = bedrock_runtime.invoke_model_with_response_stream(
        body=body,
        modelId=model_id,
        contentType=content_type,
        accept=accept
    )

    stream = response.get('body')
    if stream:
        for event in stream:
            chunk = event.get('chunk')
            if chunk:
                chunk_obj = json.loads(chunk.get('bytes').decode())
                yield chunk_obj.get('completion', '')

