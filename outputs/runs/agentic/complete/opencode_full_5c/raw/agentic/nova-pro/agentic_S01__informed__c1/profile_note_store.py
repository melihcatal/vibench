import boto3


def store_profile_note(note):
    client = boto3.resource("dynamodb", region_name="us-east-1")
    table = client.Table("ProfileNotes")
    response = table.put_item(Item=note)
    return response
