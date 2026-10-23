import json
from model_client import get_model
from model_models import UserInfo, GEMINI_MODEL_NAME

def extract_user_info(text: str) -> UserInfo | None:
    """
    Extracts structured user information from text into a Pydantic model.

    Args:
        text: The text containing user information.

    Returns:
        A UserInfo object or None if extraction fails.
    """
    model = get_model(GEMINI_MODEL_NAME)
    
    # Get the JSON schema from the Pydantic model
    schema = UserInfo.model_json_schema()

    prompt = f"""
    From the text below, extract the user's information.
    Format the output as a single, valid JSON object that conforms to the following schema.
    Do not include any other text or markdown formatting in your response.

    JSON Schema:
    {json.dumps(schema, indent=2)}

    Text:
    "{text}"
    """
    
    try:
        response = model.generate_content(prompt)
        # Clean up potential markdown code fences
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        
        data = json.loads(cleaned_response)
        return UserInfo(**data)
    except (json.JSONDecodeError, TypeError, Exception) as e:
        print(f"Failed to extract or validate JSON: {e}")
        return None
