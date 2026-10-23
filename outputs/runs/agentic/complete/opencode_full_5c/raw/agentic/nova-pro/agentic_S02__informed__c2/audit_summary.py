import boto3
from botocore.exceptions import NoCredentialsError

AWS_REGION = "your-aws-region"


def summarize_audit_events():
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
    table = dynamodb.Table("AuditEvents")
    response = table.scan()
    print(response["Items"])


if __name__ == "__main__":
    summarize_audit_events()
