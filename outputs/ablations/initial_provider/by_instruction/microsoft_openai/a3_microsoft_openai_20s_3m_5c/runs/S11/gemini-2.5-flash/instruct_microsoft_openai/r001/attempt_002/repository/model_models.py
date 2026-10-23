from typing import Dict, Any

def create_chat_request(prompt: str, model_name: str = "gpt-4o") -> Dict[str, Any]:
    return {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}]
    }

def normalize_chat_response(response: Any) -> Dict[str, Any]:
    if hasattr(response, 'choices') and response.choices:
        content = response.choices[0].message.content
        metadata = {
            "id": response.id,
            "model": response.model,
            "usage": response.usage.model_dump() if hasattr(response, 'usage') and response.usage else None,
            "finish_reason": response.choices[0].finish_reason if response.choices[0].finish_reason else None
        }
        return {"content": content, "metadata": metadata}
    return {"content": "", "metadata": {}}
