import speech_client
from typing import Dict, Any

def moderate_text_content(text: str) -> Dict[str, Any]:
    content_safety_client = speech_client.get_content_safety_client()
    response = content_safety_client.analyze_text(text=text)
    
    result = {
        "hate": response.hate.severity if response.hate else 0,
        "self_harm": response.self_harm.severity if response.self_harm else 0,
        "sexual": response.sexual.severity if response.sexual else 0,
        "violence": response.violence.severity if response.violence else 0,
    }
    return result