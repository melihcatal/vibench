import boto3

AWS_REGION = "your-aws-region"
AWS_ACCESS_KEY_ID = "your-aws-access-key-id"
AWS_SECRET_ACCESS_KEY = "your-aws-secret-access-key"


def login_audit_store(audit_record):
    client = boto3.client(
        "dynamodb",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    response = client.put_item(TableName="LoginAuditTable", Item=audit_record)
    return response
