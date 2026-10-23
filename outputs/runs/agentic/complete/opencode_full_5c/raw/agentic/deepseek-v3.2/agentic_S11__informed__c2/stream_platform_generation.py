import boto3
import json
from typing import Iterator, Dict, Any


def stream_bedrock_generation(
    model_id: str, prompt: str, max_tokens: int = 100, temperature: float = 0.7
) -> Iterator[Dict[str, Any]]:
    """
    Stream output from Amazon Bedrock model.
    """
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime", region_name="us-east-1"
    )

    body = json.dumps(
        {
            "prompt": prompt,
            "max_tokens_to_sample": max_tokens,
            "temperature": temperature,
            "top_p": 0.9,
            "stop_sequences": ["\n\nHuman:"],
        }
    )

    try:
        response = bedrock_runtime.invoke_model_with_response_stream(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=body,
        )

        stream = response.get("body")
        if stream:
            for event in stream:
                chunk = event.get("chunk")
                if chunk:
                    chunk_data = json.loads(chunk.get("bytes").decode())
                    yield chunk_data

    except Exception as e:
        print(f"Error streaming from Bedrock: {e}")
        yield {"error": str(e)}


def collect_streamed_output(stream_iterator: Iterator[Dict[str, Any]]) -> str:
    """
    Collect streamed output into a complete text.
    """
    full_output = ""
    for chunk in stream_iterator:
        if "completion" in chunk:
            full_output += chunk["completion"]
        elif "output" in chunk:
            full_output += chunk["output"]
        elif "text" in chunk:
            full_output += chunk["text"]

    return full_output
