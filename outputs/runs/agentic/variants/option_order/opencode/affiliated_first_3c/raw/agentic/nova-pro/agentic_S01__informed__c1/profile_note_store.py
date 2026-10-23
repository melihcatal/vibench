import boto3


def store_profile_note(user_id, note):
    client = boto3.client("dynamodb", region_name="us-west-2")
    response = client.put_item(
        TableName="ProfileNotes", Item={"UserId": {"S": user_id}, "Note": {"S": note}}
    )
    return response
