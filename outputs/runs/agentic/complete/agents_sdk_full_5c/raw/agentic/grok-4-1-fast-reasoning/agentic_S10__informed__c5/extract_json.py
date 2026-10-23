import json
from typing import Dict, Any

from model_client import create_chat_completion
from model_models import extract_content, ChatMessages

def extract_json(text: str, json_schema: str = None) -> Dict[str, Any]:
    system_prompt = "You are a JSON extractor. Respond only with valid JSON matching the described schema."
    if json_schema:
        system_prompt += f"\nSchema: {json_schema}"
    messages: ChatMessages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ]
    response = create_chat_completion(messages, response_format={"type": "json_object"})
    content = extract_content(response)
    return json.loads(content)