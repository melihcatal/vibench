import os
import json
from messaging_client import MessagingClient
from messaging_models import EventMessage


def consume_event(subscription_id, max_messages=1):
    client = MessagingClient()

    subscription_path = client.get_subscription_path(subscription_id)

    try:
        messages = client.pull_messages(subscription_path, max_messages)

        if not messages:
            print(
                f"No messages available in Google Cloud Pub/Sub subscription {subscription_id}"
            )
            return []

        processed_messages = []
        ack_ids = []

        for message in messages:
            try:
                event_data = EventMessage.from_json(message.message.data)
                attributes = dict(message.message.attributes)

                processed_message = {
                    "message_id": message.message.message_id,
                    "data": event_data,
                    "attributes": attributes,
                    "publish_time": message.message.publish_time,
                    "ack_id": message.ack_id,
                }

                processed_messages.append(processed_message)
                ack_ids.append(message.ack_id)

                print(
                    f"Consumed message {message.message.message_id} from Google Cloud Pub/Sub"
                )
                print(f"Event type: {event_data.event_type}")
                print(f"Source: {event_data.source}")

            except Exception as e:
                print(f"Failed to process message {message.message.message_id}: {e}")
                ack_ids.append(message.ack_id)

        if ack_ids:
            client.acknowledge_messages(subscription_path, ack_ids)
            print(f"Acknowledged {len(ack_ids)} messages")

        return processed_messages

    except Exception as e:
        print(
            f"Failed to consume messages from Google Cloud Pub/Sub subscription {subscription_id}: {e}"
        )
        raise


def process_single_event(subscription_id):
    messages = consume_event(subscription_id, max_messages=1)

    if messages:
        message = messages[0]
        event_data = message["data"]

        print(f"\nProcessing event: {event_data.event_type}")
        print(f"Payload: {json.dumps(event_data.payload, indent=2)}")

        if event_data.correlation_id:
            print(f"Correlation ID: {event_data.correlation_id}")

        return {
            "message_id": message["message_id"],
            "event_type": event_data.event_type,
            "payload": event_data.payload,
            "processed": True,
        }

    return None


if __name__ == "__main__":
    try:
        result = process_single_event("user-events-subscription")
        if result:
            print(f"\nSuccessfully processed message: {result['message_id']}")
        else:
            print("No messages to process")
    except Exception as e:
        print(f"Error: {e}")
