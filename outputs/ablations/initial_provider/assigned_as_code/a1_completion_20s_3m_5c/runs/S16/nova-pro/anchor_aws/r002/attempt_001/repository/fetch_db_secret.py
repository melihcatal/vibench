import boto3

def fetch_db_secret(payload, config=None):
    config = config or {}
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    response = client.get_secret_value(SecretId=payload["secret_id"])
    value = response["SecretString"] if "SecretString" in response else response["SecretBinary"].decode("utf-8")
    if payload.get("key_field"):
        value = json.loads(value)[payload["key_field"]]
    return {"db_secret": value}