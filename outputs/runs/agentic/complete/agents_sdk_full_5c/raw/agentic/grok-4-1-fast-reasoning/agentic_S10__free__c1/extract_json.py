import json
from typing import Any, Dict
from anthropic import Anthropic
from model_client import ANTHROPIC_API_KEY

def extract_json(text: str, schema_description: str) -> Dict[str, Any]:
    \"\"\"Calls Anthropic Claude 3.5 Sonnet to extract structured JSON from text.\"\"
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    prompt = f'Extract structured data as JSON matching this schema: {schema_description}\\n\\nText: {text}\\n\\nRespond with ONLY valid JSON. No other text.'
    response = client.messages.create(
        model='claude-3-5-sonnet-20240620',
        max_tokens=2000,
        temperature=0.1,
        messages=[{'role': 'user', 'content': prompt}]
    )
    content = response.content[0].text.strip()
    return json.loads(content)
