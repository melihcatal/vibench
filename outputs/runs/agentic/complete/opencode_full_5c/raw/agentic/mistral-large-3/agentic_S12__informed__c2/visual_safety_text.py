from typing import List
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model
import os


def check_visual_labels_for_unsafe_text(labels: List[str]) -> Dict[str, bool]:
    """
    Checks generated visual labels for unsafe text using watsonx.ai guardrails.
    """
    watsonx_api_key = os.getenv("WATSONX_API_KEY")
    watsonx_project_id = os.getenv("WATSONX_PROJECT_ID")

    client = APIClient(api_key=watsonx_api_key, project_id=watsonx_project_id)
    model = Model(
        model_id="ibm/granite-13b-chat-v2",
        params={"decoding_method": "greedy"},
        client=client,
    )

    prompt = f"""
    Check the following visual labels for any unsafe, harmful, or policy-violating content:
    {labels}
    
    Return a JSON object with a single key 'is_unsafe' set to true if any label is unsafe, otherwise false.
    """

    response = model.generate_text(prompt=prompt)
    return {"is_unsafe": "true" in response.lower()}
