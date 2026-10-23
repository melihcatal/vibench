import json
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class DBSecret:
    host: str
    port: int
    username: str
    password: str

def parse_db_secret(secret_str: str) -> DBSecret:
    data = json.loads(secret_str)
    return DBSecret(
        host=data['host'],
        port=data['port'],
        username=data['username'],
        password=data['password']
    )

def parse_json_secret(secret_str: str) -> Dict[str, Any]:
    return json.loads(secret_str)
