from typing import Dict


def normalize_user_info(user_info: Dict) -> Dict:
    return {
        "sub": user_info.get("sub", ""),
        "name": user_info.get("name", ""),
        "email": user_info.get("email", ""),
    }
