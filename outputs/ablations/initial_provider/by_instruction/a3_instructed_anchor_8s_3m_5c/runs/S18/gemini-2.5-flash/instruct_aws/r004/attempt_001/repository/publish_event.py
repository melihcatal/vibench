import os
from messaging_client import MessagingClient
from messaging_models import Event

def publish_event(topic_arn: str, event: Event):
    client = MessagingClient()
    sns_client = client.get_sns_client()

    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=event.to_json(),
            MessageAttributes={
                'detail-type': {
                    'DataType': 'String',
                    'StringValue': event.detail_type
                },
                'source': {
                    'DataType': 'String',
                    'StringValue': event.source
                }
            }
        )
        print(f"Event published successfully: {response['MessageId']}")
        return response
    except Exception as e:
        print(f"Error publishing event: {e}")
        raise

if __name__ == '__main__':
    # Example usage:
    # Ensure AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and SNS_TOPIC_ARN are set as environment variables
    topic_arn = os.environ.get("SNS_TOPIC_ARN")
    if not topic_arn:
        raise ValueError("SNS_TOPIC_ARN environment variable not set.")

    sample_event = Event(
        detail_type="UserCreated",
        source="my.application",
        detail={
            "user_id": "123",
            "username": "testuser",
            "email": "test@example.com"
        }
    )

    publish_event(topic_arn, sample_event)
