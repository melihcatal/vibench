import os
from typing import Generator
from google.cloud import aiplatform
from google.cloud.aiplatform_v1.types import prediction_service


def stream_model_generation(
    prompt: str, deployment_name: str = "text-bison"
) -> Generator[str, None, None]:
    """Stream output from a managed model platform while preserving provider response objects."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)

    endpoint = aiplatform.Endpoint(
        endpoint_name=f"projects/{project_id}/locations/{location}/endpoints/{deployment_name}"
    )

    instances = [{"content": prompt}]
    parameters = {"temperature": 0.2, "maxOutputTokens": 1024, "topP": 0.95, "topK": 40}

    try:
        response_stream = endpoint.predict_streaming(
            instances=instances, parameters=parameters
        )

        for response in response_stream:
            if hasattr(response, "predictions") and response.predictions:
                for prediction in response.predictions:
                    if isinstance(prediction, dict) and "content" in prediction:
                        yield prediction["content"]
                    elif hasattr(prediction, "content"):
                        yield prediction.content
                    else:
                        yield str(prediction)

    except Exception as e:
        yield f"Error during streaming: {str(e)}"


def stream_with_metadata(
    prompt: str, deployment_name: str = "text-bison"
) -> Generator[dict, None, None]:
    """Stream with metadata preservation."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)

    endpoint = aiplatform.Endpoint(
        endpoint_name=f"projects/{project_id}/locations/{location}/endpoints/{deployment_name}"
    )

    instances = [{"content": prompt}]
    parameters = {"temperature": 0.2, "maxOutputTokens": 1024, "topP": 0.95, "topK": 40}

    try:
        response_stream = endpoint.predict_streaming(
            instances=instances, parameters=parameters
        )

        chunk_count = 0
        for response in response_stream:
            chunk_count += 1
            chunk_data = {
                "chunk_number": chunk_count,
                "raw_response": response,
                "model_deployment": deployment_name,
                "project_id": project_id,
                "location": location,
            }

            if hasattr(response, "predictions") and response.predictions:
                predictions = []
                for pred in response.predictions:
                    if isinstance(pred, dict):
                        predictions.append(pred)
                    else:
                        predictions.append(str(pred))
                chunk_data["predictions"] = predictions

            if hasattr(response, "metadata"):
                chunk_data["metadata"] = response.metadata

            yield chunk_data

    except Exception as e:
        yield {
            "error": str(e),
            "model_deployment": deployment_name,
            "project_id": project_id,
            "location": location,
        }


if __name__ == "__main__":
    test_prompt = "Write a short story about a robot learning to paint."

    print("Streaming response chunks:")
    for chunk in stream_model_generation(test_prompt, "text-bison-32k"):
        print(chunk, end="", flush=True)
    print("\n\nStreaming with metadata:")
    for chunk_data in stream_with_metadata(test_prompt, "text-bison-32k"):
        if "predictions" in chunk_data:
            print(f"Chunk {chunk_data['chunk_number']}: {chunk_data['predictions']}")
