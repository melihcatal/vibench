import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('OnboardingNotes')


def store_note(user_id, note, metadata):
    response = table.put_item(
        Item={
            'user_id': user_id,
            'note': note,
            'metadata': metadata
        }
    )
    return response


def get_note(user_id):
    response = table.get_item(
        Key={'user_id': user_id}
    )
    return response.get('Item', None)