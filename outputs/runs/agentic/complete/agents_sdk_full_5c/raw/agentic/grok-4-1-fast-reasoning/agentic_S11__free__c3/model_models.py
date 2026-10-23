from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class PlatformUsage(BaseModel):
    prompt_tokens: Optional[int]
    completion_tokens: Optional[int]
    total_tokens: Optional[int]

def normalize_to_platform_request(
    user_prompt: str, 
    system_prompt: Optional[str] = None,
    model: Optional[str] = None
) -> Dict[str, Any]:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})
    request = {
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000,
    }
    if model:
        request["model"] = model
    return request
