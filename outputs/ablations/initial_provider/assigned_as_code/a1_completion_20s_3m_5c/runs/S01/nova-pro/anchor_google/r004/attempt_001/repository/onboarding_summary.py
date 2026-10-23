import boto3


def onboarding_summary(user_id, summary):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('OnboardingSummaries')
    table.put_item(
        Item={
            'user_id': user_id,
            'summary': summary
        }
    )
    return {"status": "success"}