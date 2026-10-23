from typing import Any, Dict, List

class DocumentModels:
    @staticmethod
    def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
        return response