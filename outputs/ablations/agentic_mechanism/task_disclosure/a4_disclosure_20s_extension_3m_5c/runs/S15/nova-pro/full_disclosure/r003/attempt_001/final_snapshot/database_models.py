from typing import Any, Dict, List, Union

class RequestModel:
    def __init__(self, document_id: str, data: Dict[str, Any]):
        self.document_id = document_id
        self.data = data

    @staticmethod
    def normalize(data: Dict[str, Any]) -> Dict[str, Any]:
        # Placeholder for normalization logic
        return data

class ResponseModel:
    def __init__(self, status: str, data: Union[Dict[str, Any], List[Dict[str, Any]]]):
        self.status = status
        self.data = data

    @staticmethod
    def normalize(data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        # Placeholder for normalization logic
        return data