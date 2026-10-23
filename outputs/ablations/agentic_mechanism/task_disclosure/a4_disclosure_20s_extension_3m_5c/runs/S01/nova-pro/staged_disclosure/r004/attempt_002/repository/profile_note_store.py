import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('OnboardingNotes')

def store_note(note_id, note_content, metadata):
    table.put_item(
        Item={
            'NoteId': note_id,
            'NoteContent': note_content,
            'Metadata': metadata
        }
    )

def get_note(note_id):
    response = table.get_item(
        Key={'NoteId': note_id}
    )
    return response.get('Item', None)