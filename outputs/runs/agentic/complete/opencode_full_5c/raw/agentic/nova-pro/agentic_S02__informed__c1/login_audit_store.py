import os
import boto3

AWS_REGION = os.getenv("AWS_REGION")


def login_audit_store(event):
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
    table = dynamodb.Table("FederatedLoginAudit")
    table.put_item(Item=event)
