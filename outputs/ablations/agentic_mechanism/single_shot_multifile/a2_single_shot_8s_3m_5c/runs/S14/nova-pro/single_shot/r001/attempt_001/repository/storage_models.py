from typing import Dict, Any

class S3Object:
    def __init__(self, key: str, metadata: Dict[str, Any]):
        self.key = key
        self.metadata = metadata

    @staticmethod
    def from_dict(obj_dict: Dict[str, Any]) -> 'S3Object':
        return S3Object(obj_dict['Key'], obj_dict['Metadata'])

    def to_dict(self) -> Dict[str, Any]:
        return {'Key': self.key, 'Metadata': self.metadata}