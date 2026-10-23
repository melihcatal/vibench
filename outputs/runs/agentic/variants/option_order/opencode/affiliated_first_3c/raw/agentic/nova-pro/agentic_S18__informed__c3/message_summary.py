import boto3


def message_summary(messages):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("MessageSummary")
    for message in messages:
        table.put_item(Item=message)
    return "Messages summarized"
