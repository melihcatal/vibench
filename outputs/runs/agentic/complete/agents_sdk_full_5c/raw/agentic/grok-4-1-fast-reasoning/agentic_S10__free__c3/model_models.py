from typing import List, Dict
import json

ChatMessage = Dict[str, str]

def build_system_user_prompt(system_prompt: str, user_prompt: str) -> List[ChatMessage]:
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

def normalize_completion(response) -> str:
    if hasattr(response, 'choices') and response.choices and len(response.choices) > 0 and hasattr(response.choices[0], 'message') and response.choices[0].message and hasattr(response.choices[0].message, 'content'):
        content = response.choices[0].message.content
        return content.strip() if content else ""
    return ""

def parse_json_completion(response) -> Dict:
    content = normalize_completion(response)
    return json.loads(content)