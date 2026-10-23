import uuid
from identity_client import AWSClient
from identity_models import ProfileNoteStoreRequest, ProfileNoteStoreResponse

def profile_note_store(request: ProfileNoteStoreRequest) -> ProfileNoteStoreResponse:
    aws_client = AWSClient()
    dynamodb_client = aws_client.get_dynamodb_client()
    table_name = 'UserProfileNotes' # This table should be pre-created in DynamoDB

    try:
        note_id = str(uuid.uuid4())
        item = {
            'noteId': {'S': note_id},
            'userId': {'S': request.user_id},
            'noteContent': {'S': request.note_content},
        }
        if request.metadata:
            item['metadata'] = {'M': {k: {'S': str(v)} for k, v in request.metadata.items()}}

        dynamodb_client.put_item(
            TableName=table_name,
            Item=item
        )
        return ProfileNoteStoreResponse(success=True, note_id=note_id, message="Note stored successfully.")
    except Exception as e:
        return ProfileNoteStoreResponse(success=False, message=f"Failed to store note: {str(e)}")
