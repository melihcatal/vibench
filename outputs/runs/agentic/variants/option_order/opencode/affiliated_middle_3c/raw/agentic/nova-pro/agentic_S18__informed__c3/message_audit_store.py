import boto3

# Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


# Persist processed message records for later lookup
def persist_message_record(record):
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    table = dynamodb.Table("your-table-name")
    table.put_item(Item=record)


if __name__ == "__main__":
    record = {"id": "1", "message": "Hello, world!"}
    persist_message_record(record)
