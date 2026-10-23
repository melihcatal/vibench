import os
import sys
import json
import boto3
from datetime import datetime
from botocore.exceptions import ClientError

region_name = os.getenv("AWS_REGION", "us-east-1")
dynamodb = boto3.resource("dynamodb", region_name=region_name)
table_name = os.getenv("AUDIT_TABLE_NAME", "MessageAudits")
table = dynamodb.Table(table_name)

if __name__ == "__main__":
    input_data = sys.stdin.read().strip()
    if not input_data:
        print(json.dumps({"error": "No input data"}))
        sys.exit(1)
    msg_data = json.loads(input_data)
    msg_data["processed_at"] = datetime.utcnow().isoformat()
    msg_data["partition_key"] = msg_data.get("message_id", "unknown")  # for dynamo PK
    try:
        table.put_item(Item=msg_data)
        print(
            json.dumps(
                {
                    "status": "stored successfully",
                    "message_id": msg_data.get("message_id"),
                }
            )
        )
    except ClientError as e:
        print(json.dumps({"error": e.response["Error"]["Message"]}))
