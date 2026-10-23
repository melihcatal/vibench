import os
from typing import List
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model
from .vision_models import LabelDetectionResponse


def visual_safety_text(
    labels: LabelDetectionResponse, api_key: str = None, project_id: str = None
) -> bool:
    """
    Checks generated visual labels for unsafe text using watsonx.ai HAP detection.
    """
    api_key = api_key or os.getenv("WATSONX_API_KEY")
    project_id = project_id or os.getenv("WATSONX_PROJECT_ID")

    if not api_key or not project_id:
        raise ValueError(
            "WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables must be set."
        )

    client = APIClient(api_key=api_key, project_id=project_id)

    model = Model(
        model_id="ibm/granite-13b-chat-v2",
        params={"decoding_method": "greedy"},
        client=client,
    )

    prompt = (
        f"Analyze the following list of visual labels detected in an image and determine if any of them "
        f"contain harmful, abusive, or policy-violating content. Labels: {', '.join(labels.labels)}. "
        f"Respond with 'UNSAFE' if any label is unsafe, otherwise respond with 'SAFE'."
    )

    response = model.generate_text(prompt=prompt)

    return "UNSAFE" in response.upper()
