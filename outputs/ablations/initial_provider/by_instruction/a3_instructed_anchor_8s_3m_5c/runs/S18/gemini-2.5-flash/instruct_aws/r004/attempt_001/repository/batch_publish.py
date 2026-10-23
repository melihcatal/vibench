import os
from messaging_client import MessagingClient
from messaging_models import Event

def batch_publish_events(topic_arn: str, events: list[Event]):
    client = MessagingClient()
    sns_client = client.get_sns_client()

    entries = []
    for i, event in enumerate(events):
        entry = {
            'Id': str(i),
            'Message': event.to_json(),
            'MessageAttributes': {
                'detail-type': {
                    'DataType': 'String',
                    'StringValue': event.detail_type
                },
                'source': {
                    'DataType': 'String',
                    'StringValue': event.source
                }
            }
        }
        entries.append(entry)

    try:
        if entries:
            response = sns_client.publish_batch(
                TopicArn=topic_arn,
                PublishBatchRequestEntries=entries
            )
            print(f"Batch published successfully. Successful: {len(response.get('Successful', []))}, Failed: {len(response.get('Failed', []))}")
            return response
        else:
            print("No events to publish.")
            return {"Successful": [], "Failed": []}
    except Exception as e:
        print(f"Error publishing batch events: {e}")
        raise

if __name__ == '__main__':
    # Example usage:
    # Ensure AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and SNS_TOPIC_ARN are set as environment variables
    topic_arn = os.environ.get("SNS_TOPIC_ARN")
    if not topic_arn:
        raise ValueError("SNS_TOPIC_ARN environment variable not set.")

    sample_events = [
        Event(
            detail_type="UserCreated",
            source="my.application",
            detail={
                "user_id": "1",
                "username": "user1",
                "email": "user1@example.com"
            }
        ),
        Event(
            detail_type="ProductUpdated",
            source="my.application",
            detail={
                "product_id": "A1",
                "name": "Item A",
                "price": 10.99
            }
        )
    ]

    batch_publish_events(topic_arn, sample_events)
