import os
import json
from typing import Dict, Any, Optional
from security_models import ApiKeySecret, DbSecret, JsonSecret

def parse_api_key_secret(secret_str: str) -> ApiKeySecret:
    return ApiKeySecret(api_key=secret_str.strip())

def parse_db_secret(secret_str: str) -> DbSecret:
    data: Dict[str, Any] = json.loads(secret_str)
    return DbSecret(
        host=data['host'],
        port=data['port'],
        username=data['username'],
        password=data['password'],
        database=data.get('database')
    )

def parse_json_secret(secret_str: str) -> JsonSecret:
    return json.loads(secret_str)

def get_secret_config(env_var: str = 'SECRET_CONFIG') -> str:
    return os.getenv(env_var, 'default')