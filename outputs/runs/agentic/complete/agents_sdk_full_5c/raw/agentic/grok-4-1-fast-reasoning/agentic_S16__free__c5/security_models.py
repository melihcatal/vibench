from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class DBConnectionSecret:
    host: str
    port: int
    username: str
    password: str
    database: str

def parse_json_secret(secret_str: str) -> Dict[str, Any]:
    import json
    return json.loads(secret_str)

def build_db_connection(secret_dict: Dict[str, Any]) -> DBConnectionSecret:
    return DBConnectionSecret(
        host=secret_dict["host"],
        port=int(secret_dict["port"]),
        username=secret_dict["username"],
        password=secret_dict["password"],
        database=secret_dict["database"]
    )
