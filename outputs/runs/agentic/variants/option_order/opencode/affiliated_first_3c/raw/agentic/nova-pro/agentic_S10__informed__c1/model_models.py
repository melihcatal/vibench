from typing import Dict


def normalize_request(
    text: str, max_tokens: int = 512, temperature: float = 0.5, top_p: float = 0.9
) -> Dict:
    return {
        "inputText": text,
        "textGenerationConfig": {
            "maxTokenCount": max_tokens,
            "temperature": temperature,
            "topP": top_p,
        },
    }


def normalize_response(response):
    return response["outputText"]
