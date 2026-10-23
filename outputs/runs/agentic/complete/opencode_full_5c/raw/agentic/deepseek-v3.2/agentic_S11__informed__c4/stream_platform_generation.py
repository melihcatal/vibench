import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import ModelInference


def stream_model_generation(prompt, model_id=None, parameters=None):
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")

    if not api_key or not project_id:
        raise ValueError(
            "WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables must be set"
        )

    client = APIClient(api_key=api_key, project_id=project_id)

    if model_id is None:
        model_id = "ibm/granite-13b-chat-v2"

    if parameters is None:
        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 100,
            "min_new_tokens": 1,
            "temperature": 0.7,
            "stream": True,
        }

    model = ModelInference(
        model_id=model_id,
        params=parameters,
        credentials={"apikey": api_key, "url": "https://us-south.ml.cloud.ibm.com"},
        project_id=project_id,
    )

    stream_response = model.generate_stream(prompt=prompt)

    for chunk in stream_response:
        if hasattr(chunk, "choices") and chunk.choices:
            for choice in chunk.choices:
                if hasattr(choice, "text"):
                    yield choice.text
                elif hasattr(choice, "delta") and hasattr(choice.delta, "content"):
                    yield choice.delta.content
        elif hasattr(chunk, "generated_text"):
            yield chunk.generated_text
