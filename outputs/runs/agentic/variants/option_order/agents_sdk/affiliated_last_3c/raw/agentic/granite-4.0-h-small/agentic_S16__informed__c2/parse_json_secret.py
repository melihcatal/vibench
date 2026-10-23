import os
import json
from aws_secretsmanager import get_secret

def parse_json_secret(secret_name='CONFIG'):
    raw_blob = get_secret(secret_name)
    return json.loads(raw_blob)
