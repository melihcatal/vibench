import json

from identity_client import dynamodb_resource, load_identity_config, s3_client


def profile_note_store(account_id: str, note: str, support_metadata: dict):
    config = load_identity_config()
    table = dynamodb_resource().Table(config.support_table_name)
    s3 = s3_client()
    key = f"notes/{account_id}.json"
    body = json.dumps({"account_id": account_id, "note": note, "support_metadata": support_metadata})
    s3.put_object(Bucket=config.support_bucket, Key=key, Body=body.encode("utf-8"), ContentType="application/json")
    table.put_item(Item={"account_id": account_id, "note_s3_key": key, "support_metadata": support_metadata})
    return {"account_id": account_id, "note_s3_key": key}
