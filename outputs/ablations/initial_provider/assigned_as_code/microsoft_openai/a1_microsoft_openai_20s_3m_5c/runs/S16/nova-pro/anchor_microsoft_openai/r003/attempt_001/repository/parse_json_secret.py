import json
from fetch_db_secret import fetch_db_secret

def parse_json_secret(secret_name):
    secret_string = fetch_db_secret(secret_name)
    return json.loads(secret_string)