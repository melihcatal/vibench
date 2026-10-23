from typing import Any, Dict

class DatabaseModels:
    @staticmethod
    def normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'id': item['id'],
            'name': item['name'],
            'age': item['age']
        }

    @staticmethod
    def deserialize_item(item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'id': item['id'],
            'name': item['name'],
            'age': item['age']
        }