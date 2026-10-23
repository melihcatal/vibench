import boto3

def summarize_onboarding_state():
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.scan(TableName='OnboardingTable')
    items = response.get('Items', [])
    summary = {'total': len(items), 'completed': 0, 'in_progress': 0, 'pending': 0}
    for item in items:
        status = item.get('status', {}).get('S', 'pending')
        if status == 'completed':
            summary['completed'] += 1
        elif status == 'in_progress':
            summary['in_progress'] += 1
        else:
            summary['pending'] += 1
    return summary

if __name__ == '__main__':
    print(summarize_onboarding_state())