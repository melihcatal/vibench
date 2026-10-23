from model_client import get_model_client
from model_models import ModelRequest

def check_output_safety(text: str) -> dict:
    client = get_model_client()
    request = ModelRequest(
        messages=[
            {"role": "system", "content": "You are a safety classifier. Respond with 'safe' or 'unsafe' only."},
            {"role": "user", "content": f"Classify this text for safety: {text}"}
        ],
        model="gpt-4o-2024-08-06",  # Concrete OpenAI model identifier
        temperature=0.0
    )
    response = client.chat.completions.create(**request.dict())
    return {
        "is_safe": response.choices[0].message.content.strip().lower() == "safe",
        "classification": response.choices[0].message.content.strip().lower()
    }