import json
from typing import Any

def normalize_response(event: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize a streaming response into a simple dict (interim, transcript).""",
    result = {}
    alternatives = event.get("results", [{}])[0].get("alternatives", [])
    if alternatives:
        best = alternatives[0]
        result["interim"] = best.get("interim")
        result["transcript"] = best.get("transcript")
    return result

if __name__ == "__main__":
    sample = {
        "results": [
            {
                "alternatives": [
                    {
                        "interim": "Hello",
                        "transcript": "Hello"
                    }
                ]
            }
        ]
    }
    print(normalize_response(sample))
