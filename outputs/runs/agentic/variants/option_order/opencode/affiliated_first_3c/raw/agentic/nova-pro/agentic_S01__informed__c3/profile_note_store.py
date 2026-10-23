import boto3


def store_profile_note(user_id, note):
    client = boto3.client("dynamodb", region_name="us-west-2")
    response = client.put_item(
        TableName="OnboardingNotes",
        Item={"user_id": {"S": user_id}, "note": {"S": note}},
    )
    return response
