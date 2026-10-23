from typing import Dict, Any

def normalize_message(message: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'body': message.get('Body', ''),
        'attributes': message.get('MessageAttributes', {})
    }