from typing import List, Dict, Optional

def build_chat_messages(
    prompt: str,
    system_prompt: Optional[str] = None
) -> List[Dict[str, str]]:
    messages: List[Dict[str, str]] = []
    if system_prompt:
        messages.append({'role': 'system', 'content': system_prompt})
    messages.append({'role': 'user', 'content': prompt})
    return messages
