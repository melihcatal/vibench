import json
from model_client import get_client
from model_models import CompletionRequest


def extract_json(text: str) -> dict:
    client = get_client()
    request = CompletionRequest(
        prompt=f"Extract the JSON object from the following text. Respond with only the JSON object:\n\n{text}",
        model="gpt-4o",
    )
    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=[{"role": "user", "content": request.prompt}],
            response_format={"type": "json_object"},
        )
        json_string = response.choices[0].message.content
        return json.loads(json_string) if json_string else {}
    except (json.JSONDecodeError, IndexError, Exception) as e:
        print(f"An error occurred: {e}")
        return {}
