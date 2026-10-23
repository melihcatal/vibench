import boto3


def store_profile_note(note):
    client = boto3.client("dynamodb", region_name="us-east-1")
    response = client.put_item(
        TableName="ProfileNotes", Item={"NoteId": {"S": "12345"}, "Note": {"S": note}}
    )
    return response
