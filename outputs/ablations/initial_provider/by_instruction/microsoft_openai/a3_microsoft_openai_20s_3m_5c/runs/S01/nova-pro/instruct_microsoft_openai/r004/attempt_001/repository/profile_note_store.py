import boto3

def store_note(note):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('OnboardingNotes')
    table.put_item(Item=note)
