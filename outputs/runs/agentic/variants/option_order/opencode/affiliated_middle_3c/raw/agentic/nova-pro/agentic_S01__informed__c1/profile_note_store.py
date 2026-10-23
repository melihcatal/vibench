import boto3


def store_profile_note(user_id, note):
    dynamodb_client = boto3.client("dynamodb")
    response = dynamodb_client.put_item(
        TableName="OnboardingNotes",
        Item={"user_id": {"S": user_id}, "note": {"S": note}},
    )
    return response
