import boto3
import json
import os
from typing import Dict, Any
from datetime import datetime


def invoke_with_metadata(
    model_id: str, prompt: str, max_tokens: int = 1000, temperature: float = 0.7
) -> Dict[str, Any]:
    """
    Invoke Bedrock model and collect comprehensive metadata.
    """
    bedrock_runtime = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    start_time = datetime.now()

    if "anthropic" in model_id:
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt}],
            }
        )
    elif "meta" in model_id:
        body = json.dumps(
            {"prompt": prompt, "max_gen_len": max_tokens, "temperature": temperature}
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
            {"prompt": prompt, "max_tokens": max_tokens, "temperature": temperature}
        )

    try:
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=body,
        )

        end_time = datetime.now()
        latency = (end_time - start_time).total_seconds()

        response_body = json.loads(response["body"].read())

        metadata = {
            "model_id": model_id,
            "invocation_timestamp": start_time.isoformat(),
            "latency_seconds": latency,
            "request_id": response.get("ResponseMetadata", {}).get("RequestId"),
            "http_status_code": response.get("ResponseMetadata", {}).get(
                "HTTPStatusCode"
            ),
            "retry_attempts": response.get("ResponseMetadata", {}).get(
                "RetryAttempts", 0
            ),
            "request_parameters": {
                "max_tokens": max_tokens,
                "temperature": temperature,
                "prompt_length": len(prompt),
            },
        }

        if "anthropic" in model_id:
            text = response_body["content"][0]["text"]
            usage = response_body.get("usage", {})
            metadata.update(
                {
                    "text": text,
                    "usage": {
                        "input_tokens": usage.get("input_tokens", 0),
                        "output_tokens": usage.get("output_tokens", 0),
                        "total_tokens": usage.get("total_tokens", 0),
                    },
                    "stop_reason": response_body.get("stop_reason"),
                    "stop_sequence": response_body.get("stop_sequence"),
                }
            )
        elif "meta" in model_id:
            text = response_body["generation"]
            metadata.update(
                {
                    "text": text,
                    "prompt_token_count": response_body.get("prompt_token_count"),
                    "generation_token_count": response_body.get(
                        "generation_token_count"
                    ),
                    "stop_reason": response_body.get("stop_reason"),
                }
            )
        elif "amazon" in model_id:
            text = response_body["results"][0]["outputText"]
            metadata.update(
                {
                    "text": text,
                    "input_token_count": response_body.get("inputTextTokenCount"),
                    "results": response_body.get("results", []),
                    "completion_reason": response_body["results"][0].get(
                        "completionReason"
                    )
                    if response_body.get("results")
                    else None,
                }
            )
        else:
            text = response_body.get(
                "completion", response_body.get("generated_text", "")
            )
            metadata.update({"text": text, "response_body": response_body})

        metadata["response_length"] = len(text)

        return metadata

    except Exception as e:
        end_time = datetime.now()
        return {
            "model_id": model_id,
            "invocation_timestamp": start_time.isoformat(),
            "error": str(e),
            "latency_seconds": (end_time - start_time).total_seconds(),
            "http_status_code": 500,
        }


def get_model_invocation_logs(
    start_time: datetime, end_time: datetime, model_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Retrieve invocation logs from CloudWatch for Bedrock models.
    """
    cloudwatch = boto3.client(
        "cloudwatch",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    metric_name = "InvocationCount"
    namespace = "AWS/Bedrock"

    dimensions = []
    if model_id:
        dimensions.append({"Name": "ModelId", "Value": model_id})

    try:
        response = cloudwatch.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions,
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=["Sum", "Average", "SampleCount"],
        )

        datapoints = response.get("Datapoints", [])
        logs = []
        for dp in datapoints:
            logs.append(
                {
                    "timestamp": dp["Timestamp"].isoformat(),
                    "invocation_count": dp.get("Sum", 0),
                    "average_latency": dp.get("Average", 0),
                    "sample_count": dp.get("SampleCount", 0),
                    "model_id": model_id or "all_models",
                }
            )

        return sorted(logs, key=lambda x: x["timestamp"])
    except Exception as e:
        print(f"Error retrieving logs: {e}")
        return []
