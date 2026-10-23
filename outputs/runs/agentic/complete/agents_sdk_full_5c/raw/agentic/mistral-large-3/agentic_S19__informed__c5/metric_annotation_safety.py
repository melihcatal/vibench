from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model
from observability_client import get_client_config


def check_metric_annotation_safety(text: str) -> Dict[str, Any]:
    config = get_client_config()
    api_key = config.get("WATSONX_API_KEY")
    project_id = config.get("WATSONX_PROJECT_ID")
    
    if not api_key or not project_id:
        raise ValueError("WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables are required.")
    
    client = APIClient(api_key=api_key)
    client.set_project(project_id)
    
    model = Model(
        model_id="ibm/granite-13b-chat-v2",
        params={
            "decoding_method": "greedy",
            "max_new_tokens": 100,
        },
        client=client,
    )
    
    prompt = (
        "Analyze the following text for harmful, abusive, or inappropriate content. "
        "Respond with a JSON object containing 'is_safe' (boolean) and 'reason' (string).\n\n"
        f"Text: {text}"
    )
    
    response = model.generate_text(prompt)
    return {"is_safe": "harmful" not in response.lower(), "reason": response}