import boto3

def store_note(note):
    client = boto3.client('dynamodb')
    response = client.put_item(
        TableName='OnboardingNotes',
        Item={'NoteId': {'S': '1'}, 'Note': {'S': note}}
    )
    return response