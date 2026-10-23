import os
import json

class SafetyModels:
    """Utility module for request/response payload shaping and normalization."
    @staticmethod
    def build_payload(text: str) -> dict:
        """Create payload matching Azure AI Content Safety API expectations."""
        return {
            "input": {
                "type": "text",
                "text": text
            }
        }

    @staticmethod
    def normalize_response(raw: dict) -> dict:
        """Convert Azure response to a simplified internal format."""
        normalized = {
            "result": raw.get('result'),  # 'safe' or 'unsafe'
            "categories": raw.get('categories', []),  # list of dicts with name/score
            "flags": raw.get('flags', [])  # list of {'start': int, 'end': int}
        }
        return normalized

if __name__ == "__main__":
    sample = SafetyModels.build_payload("Test input")
    print(sample)
    print(SafetyModels.normalize_response({}))
