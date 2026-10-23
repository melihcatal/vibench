from typing import Dict


class UserProfile:
    def __init__(self, user_id: str, email: str, name: str):
        self.user_id = user_id
        self.email = email
        self.name = name

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(data["id"], data["mail"], data["displayName"])
