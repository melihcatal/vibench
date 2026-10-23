from typing import Any, Dict, List

class RequestHelper:
    def __init__(self, table_name: str):
        self.table_name = table_name

    def create_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'TableName': self.table_name,
            'Item': item
        }

    def get_item(self, key: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'TableName': self.table_name,
            'Key': key
        }

class ResponseHelper:
    @staticmethod
    def parse_response(response: Dict[str, Any]) -> Dict[str, Any]:
        if 'Item' in response:
            return response['Item']
        return {}

class NormalizationHelper:
    @staticmethod
    def normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
        normalized_item = {}
        for key, value in item.items():
            if isinstance(value, dict):
                normalized_item[key] = NormalizationHelper.normalize_item(value)
            else:
                normalized_item[key] = value
        return normalized_item
