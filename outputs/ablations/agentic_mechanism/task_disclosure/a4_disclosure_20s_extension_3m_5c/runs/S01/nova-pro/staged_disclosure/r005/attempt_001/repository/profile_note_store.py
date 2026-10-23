import boto3

dynamodb = boto3.resource('dynamodb')

table_name = 'OnboardingNotes'

def create_note(user_id, note, metadata):
    table = dynamodb.Table(table_name)
    response = table.put_item(
        Item={
            'user_id': user_id,
            'note': note,
            'metadata': metadata
        }
    )
    return response

def get_note(user_id):
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={'user_id': user_id}
    )
    return response.get('Item', None)
