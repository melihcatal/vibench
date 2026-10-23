import boto3

dynamodb = boto3.resource('dynamodb')


def store_profile_note(user_id, note):
    table = dynamodb.Table('OnboardingNotes')
    response = table.put_item(
        Item={
            'user_id': user_id,
            'note': note
        }
    )
    return response


def get_profile_note(user_id):
    table = dynamodb.Table('OnboardingNotes')
    response = table.get_item(
        Key={'user_id': user_id}
    )
    return response.get('Item', None)