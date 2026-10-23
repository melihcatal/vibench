import os
from typing import Dict, Any
from google.cloud import aiplatform
from datetime import datetime


def invoke_with_metadata(
    prompt: str, deployment_name: str = "text-bison"
) -> Dict[str, Any]:
    """Return model output together with provider platform metadata."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)

    endpoint = aiplatform.Endpoint(
        endpoint_name=f"projects/{project_id}/locations/{location}/endpoints/{deployment_name}"
    )

    instances = [{"content": prompt}]
    parameters = {"temperature": 0.2, "maxOutputTokens": 256, "topP": 0.95, "topK": 40}

    start_time = datetime.now()
    response = endpoint.predict(instances=instances, parameters=parameters)
    end_time = datetime.now()

    result = {
        "timestamp": start_time.isoformat(),
        "model_deployment": deployment_name,
        "project_id": project_id,
        "location": location,
        "endpoint_resource": endpoint.resource_name,
        "latency_ms": int((end_time - start_time).total_seconds() * 1000),
        "raw_response": response,
        "content": "",
        "metadata": {},
    }

    if hasattr(response, "predictions") and response.predictions:
        if len(response.predictions) > 0:
            pred = response.predictions[0]
            if isinstance(pred, dict) and "content" in pred:
                result["content"] = pred["content"]
            elif hasattr(pred, "content"):
                result["content"] = pred.content
            else:
                result["content"] = str(pred)

    if hasattr(response, "metadata"):
        result["metadata"] = response.metadata

    if hasattr(response, "model_version_id"):
        result["model_version"] = response.model_version_id

    if hasattr(response, "model_display_name"):
        result["model_display_name"] = response.model_display_name

    usage_data = extract_usage_metadata(response)
    if usage_data:
        result["usage"] = usage_data

    return result


def extract_usage_metadata(response) -> Dict[str, Any]:
    """Extract usage information from Vertex AI response."""
    usage = {}

    if hasattr(response, "metadata"):
        metadata = response.metadata
        if isinstance(metadata, dict):
            if "tokenMetadata" in metadata:
                token_meta = metadata["tokenMetadata"]
                if "inputTokenCount" in token_meta:
                    usage["input_tokens"] = token_meta["inputTokenCount"].get(
                        "totalTokens", 0
                    )
                if "outputTokenCount" in token_meta:
                    usage["output_tokens"] = token_meta["outputTokenCount"].get(
                        "totalTokens", 0
                    )
            elif "usageMetadata" in metadata:
                usage_meta = metadata["usageMetadata"]
                usage["input_tokens"] = usage_meta.get("promptTokenCount", 0)
                usage["output_tokens"] = usage_meta.get("candidatesTokenCount", 0)
                usage["total_tokens"] = usage_meta.get("totalTokenCount", 0)

    return usage


def batch_invoke_with_metadata(
    prompts: list, deployment_name: str = "text-bison"
) -> list:
    """Batch invoke with metadata collection."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)

    endpoint = aiplatform.Endpoint(
        endpoint_name=f"projects/{project_id}/locations/{location}/endpoints/{deployment_name}"
    )

    instances = [{"content": prompt} for prompt in prompts]
    parameters = {"temperature": 0.2, "maxOutputTokens": 256, "topP": 0.95, "topK": 40}

    start_time = datetime.now()
    response = endpoint.predict(instances=instances, parameters=parameters)
    end_time = datetime.now()

    results = []
    if hasattr(response, "predictions") and response.predictions:
        for i, pred in enumerate(response.predictions):
            result = {
                "timestamp": start_time.isoformat(),
                "model_deployment": deployment_name,
                "prompt_index": i,
                "latency_ms": int((end_time - start_time).total_seconds() * 1000),
                "content": str(pred)
                if not isinstance(pred, dict)
                else pred.get("content", str(pred)),
            }
            results.append(result)

    return results


if __name__ == "__main__":
    test_prompt = "What are the benefits of renewable energy?"
    result = invoke_with_metadata(test_prompt, "text-bison-32k")
    print(f"Content: {result['content'][:100]}...")
    print(f"Metadata keys: {list(result.keys())}")
    if "usage" in result:
        print(f"Usage: {result['usage']}")
