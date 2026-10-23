import json
import os
import boto3


def persist_message_record(record):
    table = boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION", "us-east-1")).Table(os.environ["AUDIT_TABLE_NAME"])
    table.put_item(Item=record)
    return {"stored": True, "id": record.get("id")}


def main():
    record = json.loads(input())
    print(json.dumps(persist_message_record(record)))


if __name__ == "__main__":
    main()
