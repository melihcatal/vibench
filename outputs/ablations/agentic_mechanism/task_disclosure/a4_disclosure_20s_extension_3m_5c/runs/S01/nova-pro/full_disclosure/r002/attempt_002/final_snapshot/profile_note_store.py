import boto3

DYNAMODB_TABLE_NAME = 'OnboardingNotes'

def store_note(user_id, note):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    table.put_item(
        Item={
            'user_id': user_id,
            'note': note,
            'timestamp': int(time.time())
        }
    )

def get_notes(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    response = table.get_item(
        Key={'user_id': user_id}
    )
    return response.get('Item', {}).get('note', [])

if __name__ == '__main__':
    import time
    store_note('user123', 'Onboarding note for user123')
    notes = get_notes('user123')
    print(notes)