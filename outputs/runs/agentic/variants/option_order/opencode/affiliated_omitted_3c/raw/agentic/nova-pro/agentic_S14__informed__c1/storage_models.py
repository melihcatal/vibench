from typing import Dict, Any


class FileInfo:
    def __init__(self, file_info: Dict[str, Any]):
        self.file_info = file_info

    def to_dict(self):
        return self.file_info
