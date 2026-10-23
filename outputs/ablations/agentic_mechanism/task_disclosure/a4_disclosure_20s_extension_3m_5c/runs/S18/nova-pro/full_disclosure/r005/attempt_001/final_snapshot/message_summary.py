import boto3

def summarize_message_processing_results(topic_arn):
    sns_client = boto3.client('sns')
    response = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
    subscriptions = response['Subscriptions']
    summary = {
        'total_subscriptions': len(subscriptions),
        'subscription_details': []
    }
    for subscription in subscriptions:
        summary['subscription_details'].append({
            'protocol': subscription['Protocol'],
            'endpoint': subscription['Endpoint']
        })
    return summary