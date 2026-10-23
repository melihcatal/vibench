from model_client import GeminiClient
from model_models import JsonExtractionResult

def extract_json(payload: dict, config: dict = None) -> JsonExtractionResult:
    config = config or {}
    client = GeminiClient(api_key=config.get("api_key"), model_name="gemini-2.5-flash")
    prompt = (
        "Extract structured JSON from the following text. "
        "Ensure the output is a valid JSON object. Text:\n\n" + payload["text"]
    )
    response = client.generate_content(prompt)
    try:
        # Attempt to parse the response text as JSON. Assume the model outputs raw JSON.
        import json
        json_data = json.loads(response.text.strip())
        return JsonExtractionResult(json_data=json_data)
    except json.JSONDecodeError:
        # If the model doesn't output perfect JSON, try to find a JSON block
        import re
        match = re.search(r"```json\n(.*)\n```", response.text, re.DOTALL)
        if match:
            try:
                json_data = json.loads(match.group(1))
                return JsonExtractionResult(json_data=json_data)
            except json.JSONDecodeError:
                pass
        return JsonExtractionResult(json_data={})
