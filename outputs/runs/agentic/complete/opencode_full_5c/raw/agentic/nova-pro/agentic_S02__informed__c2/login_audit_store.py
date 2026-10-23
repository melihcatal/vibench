import boto3
from botocore.exceptions import NoCredentialsError

AWS_REGION = "your-aws-region"


def store_audit_record(record: dict):
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
    table = dynamodb.Table("AuditRecords")
    table.put_item(Item=record)


if __name__ == "__main__":
    store_audit_record({"user_id": "user-1", "event": "login"})
