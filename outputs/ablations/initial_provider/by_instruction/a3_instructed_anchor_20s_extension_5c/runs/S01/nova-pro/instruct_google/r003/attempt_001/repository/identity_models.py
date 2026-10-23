from typing import Any, Dict

class UserInfo:
    def __init__(self, id: str, email: str, name: str):
        self.id = id
        self.email = email
        self.name = name

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'UserInfo':
        return UserInfo(data.get('id'), data.get('email'), data.get('name'))