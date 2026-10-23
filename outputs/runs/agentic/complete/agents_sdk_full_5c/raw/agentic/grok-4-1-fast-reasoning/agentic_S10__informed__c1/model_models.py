from typing import Dict

def mk_system(content: str) -> Dict[str, str]:
    return {'role': 'system', 'content': content}

def mk_user(content: str) -> Dict[str, str]:
    return {'role': 'user', 'content': content}

def mk_assistant(content: str) -> Dict[str, str]:
    return {'role': 'assistant', 'content': content}
