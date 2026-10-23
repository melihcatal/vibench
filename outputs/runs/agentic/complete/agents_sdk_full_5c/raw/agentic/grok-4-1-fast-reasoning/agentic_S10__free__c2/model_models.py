def extract_completion_content(response) -> str:
    """Normalize chat completion response to content."""
    return response.choices[0].message.content.strip()

def parse_json_response(response) -> dict:
    """Parse JSON from chat completion response."""
    import json
    content = extract_completion_content(response)
    return json.loads(content)