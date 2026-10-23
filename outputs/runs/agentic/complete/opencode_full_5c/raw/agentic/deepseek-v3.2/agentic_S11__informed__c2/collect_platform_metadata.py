import boto3
import json
from typing import Dict, Any
from datetime import datetime


def invoke_bedrock_with_metadata(
    model_id: str, prompt: str, max_tokens: int = 100, temperature: float = 0.7
) -> Dict[str, Any]:
    """
    Invoke Bedrock model and collect metadata along with output.
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

    start_time = datetime.utcnow()

    try:
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=body,
        )

        end_time = datetime.utcnow()
        latency_ms = int((end_time - start_time).total_seconds() * 1000)

        response_body = json.loads(response["body"].read())

        metadata = {
            "model_id": model_id,
            "invocation_timestamp": start_time.isoformat(),
            "latency_ms": latency_ms,
            "response_headers": dict(response["ResponseMetadata"]["HTTPHeaders"]),
            "request_id": response["ResponseMetadata"]["RequestId"],
            "http_status_code": response["ResponseMetadata"]["HTTPStatusCode"],
        }

        if "usage" in response_body:
            metadata["usage"] = response_body["usage"]
        elif (
            "amazon-bedrock-invocationMetrics"
            in response["ResponseMetadata"]["HTTPHeaders"]
        ):
            metrics = response["ResponseMetadata"]["HTTPHeaders"][
                "amazon-bedrock-invocationMetrics"
            ]
            metadata["invocation_metrics"] = json.loads(metrics)

        return {
            "output": response_body.get("completion", ""),
            "raw_response": response_body,
            "metadata": metadata,
        }

    except Exception as e:
        return {
            "output": "",
            "error": str(e),
            "metadata": {
                "model_id": model_id,
                "invocation_timestamp": start_time.isoformat(),
                "error": True,
            },
        }
