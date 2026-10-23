import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.hai.llm import TextGenerationSession


def extract_json(input_text: str, schema: dict) -> dict:
    """Extract structured JSON from text using watsonx.ai hosted LLM.

    Provider: IBM watsonx.ai
    """
    api_key = os.getenv("WATSONX_API_KEY", "<INSERT_WATSONX_API_KEY>")
    project_id = os.getenv("WATSONX_PROJECT_ID", "<INSERT_WATSONX_PROJECT_ID>")
    client = APIClient(
        api_key=api_key,
        project_id=project_id,
        url="https://api.watsonx.ai",
    )
    session = TextGenerationSession(
        model_id="ibm/granite-20m-uncased",
        api_client=client,
    )
    # Define a system prompt that asks the model to return JSON matching the given schema.
    system_prompt = f"You are a JSON extractor. Transform the following text into a JSON object that conforms to this schema:\n{schema}\n\nText:\n{input_text}\n"
    response = session.generate(
        system_prompt=system_prompt, user_input="", max_new_tokens=512
    )
    json_str = response[0].get("text", "")
    # Simple safety parsing; real code should validate against schema.
    import json

    try:
        return json.loads(json_str)
    except Exception:
        return {}
