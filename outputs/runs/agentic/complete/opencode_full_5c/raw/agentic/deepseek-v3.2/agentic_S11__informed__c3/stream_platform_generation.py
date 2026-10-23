import boto3
import json
import os
from typing import Dict, Any, Generator


def stream_bedrock_generation(
    model_id: str, prompt: str, max_tokens: int = 1000, temperature: float = 0.7
) -> Generator[Dict[str, Any], None, None]:
    """
    Stream output from Amazon Bedrock while preserving provider response objects.
    """
    bedrock_runtime = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    if "anthropic" in model_id:
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt}],
                "stream": True,
            }
        )
    elif "meta" in model_id:
        body = json.dumps(
            {
                "prompt": prompt,
                "max_gen_len": max_tokens,
                "temperature": temperature,
                "stream": True,
            }
        )
    elif "amazon" in model_id:
        body = json.dumps(
            {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": max_tokens,
                    "temperature": temperature,
                },
            }
        )
    else:
        body = json.dumps(
            {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": True,
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
        if not stream:
            yield {"error": "No response stream available"}
            return

        full_text = ""
        for event in stream:
            if "chunk" in event:
                chunk = event["chunk"]
                chunk_data = json.loads(chunk.get("bytes", b"{}").decode("utf-8"))

                if "anthropic" in model_id:
                    if "delta" in chunk_data:
                        text = chunk_data["delta"].get("text", "")
                        full_text += text
                        yield {
                            "text": text,
                            "full_text": full_text,
                            "chunk": chunk_data,
                            "model_id": model_id,
                            "type": "text_delta",
                        }
                    elif "message" in chunk_data:
                        yield {
                            "message": chunk_data["message"],
                            "model_id": model_id,
                            "type": "message",
                        }
                elif "meta" in model_id:
                    if "generation" in chunk_data:
                        text = chunk_data["generation"]
                        full_text += text
                        yield {
                            "text": text,
                            "full_text": full_text,
                            "chunk": chunk_data,
                            "model_id": model_id,
                            "type": "text_delta",
                        }
                elif "amazon" in model_id:
                    if "outputText" in chunk_data:
                        text = chunk_data["outputText"]
                        full_text += text
                        yield {
                            "text": text,
                            "full_text": full_text,
                            "chunk": chunk_data,
                            "model_id": model_id,
                            "type": "text_delta",
                        }
                else:
                    if "completion" in chunk_data:
                        text = chunk_data["completion"]
                        full_text += text
                        yield {
                            "text": text,
                            "full_text": full_text,
                            "chunk": chunk_data,
                            "model_id": model_id,
                            "type": "text_delta",
                        }

        yield {
            "complete": True,
            "final_text": full_text,
            "model_id": model_id,
            "type": "completion",
        }

    except Exception as e:
        yield {"error": str(e), "model_id": model_id, "type": "error"}
