import os
import json
from model_client import GeminiClient
from model_models import ChatMessage, GenerateContentRequest


def extract_json(text: str, model_name: str = "gemini-pro") -> dict:
    """
    Calls a hosted LLM (Gemini API) to extract structured JSON from text.
    """
    gemini_client = GeminiClient().get_model(model_name)
    prompt = f"Extract a JSON object containing 'name' and 'age' from the following text:\n\n{text}\n\nReturn only the JSON object."

    request = GenerateContentRequest(
        contents=[ChatMessage(role="user", content=prompt)],
        model=model_name,
        temperature=0.1,
        max_output_tokens=100,
    )

    response = gemini_client.generate_content(
        contents=[
            {"role": msg.role, "parts": [{"text": msg.content}]}
            for msg in request.contents
        ],
        generation_config={
            "temperature": request.temperature,
            "max_output_tokens": request.max_output_tokens,
        },
    )

    json_str = ""
    for candidate in response.candidates:
        if candidate.content and candidate.content.parts:
            for part in candidate.content.parts:
                if hasattr(part, "text"):
                    json_str += part.text

    try:
        return json.loads(json_str.strip())
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from response: {json_str}")
        return {}


if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_API_KEY is set in your environment
    os.environ["GOOGLE_API_KEY"] = os.environ.get(
        "GOOGLE_API_KEY", "YOUR_GEMINI_API_KEY"
    )

    sample_text = "The user's name is Alice and she is 30 years old."
    # extracted_data = extract_json(sample_text)
    # print(f"Extracted JSON: {extracted_data}")
