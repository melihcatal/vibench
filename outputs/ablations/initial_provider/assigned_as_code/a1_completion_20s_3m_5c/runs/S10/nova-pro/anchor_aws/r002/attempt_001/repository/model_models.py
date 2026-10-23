from typing import Dict

def normalize_request(input_text: str, max_tokens: int = 2048, temperature: float = 0.5, top_p: float = 0.9) -> Dict:
    return {
        'inputText': input_text,
        'textGenerationConfig': {
            'maxTokenCount': max_tokens,
            'temperature': temperature,
            'topP': top_p
        }
    }

def parse_response(response: Dict) -> str:
    return response.get('results')[0].get('outputText')