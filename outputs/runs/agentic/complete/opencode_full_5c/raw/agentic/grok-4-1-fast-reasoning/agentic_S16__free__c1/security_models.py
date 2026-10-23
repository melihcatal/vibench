from typing import TypedDict, Optional, Dict, Any, List
import json

class DbSecret(TypedDict):
    host: str
    port: Optional[int]
    username: str
    password: str
    database: Optional[str]

class RotationSummary(TypedDict):
    enabled: bool
    lambda_arn: Optional[str]
    rules: Dict[str, Any]

def normalize_json_secret(secret_str: str) -&gt; Optional[Dict[str, Any]]:
    try:
        return json.loads(secret_str)
    except json.JSONDecodeError:
        return None

def normalize_db_secret(data: Dict[str, Any]) -&gt; Optional[DbSecret]:
    if isinstance(data, dict) and all(key in data for key in [&#x27;host&#x27;, &#x27;username&#x27;, &#x27;password&#x27;]):
        return data  # type ignore
    return None
