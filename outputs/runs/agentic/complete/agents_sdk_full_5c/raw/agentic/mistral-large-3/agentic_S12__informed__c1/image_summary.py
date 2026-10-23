import os
from typing import Dict, Any
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model
from vision_models import LabelDetectionResponse, ImageDescriptionResponse, TextDetectionResponse


def summarize_visual_analysis(
    labels: LabelDetectionResponse,
    description: ImageDescriptionResponse,
    text: TextDetectionResponse
) -> str:
    """Summarize visual analysis results using watsonx.ai Granite model."""
    watsonx_api_key = os.getenv("WATSONX_API_KEY")
    watsonx_project_id = os.getenv("WATSONX_PROJECT_ID")
    watsonx_url = "https://us-south.ml.cloud.ibm.com"

    client = APIClient(
        api_key=watsonx_api_key,
        url=watsonx_url
    )
    client.set_project_id(watsonx_project_id)

    model = Model(
        model_id="ibm/granite-13b-chat-v2",
        params={
            "decoding_method": "greedy",
            "max_new_tokens": 200
        },
        client=client
    )

    prompt = f"""
    Summarize the following visual analysis of an image:
    - Detected labels: {', '.join(labels.labels)}
    - Description: {description.description}
    - Detected text: {text.text}
    Provide a concise summary in 2-3 sentences.
    """

    response = model.generate_text(prompt=prompt)
    return response