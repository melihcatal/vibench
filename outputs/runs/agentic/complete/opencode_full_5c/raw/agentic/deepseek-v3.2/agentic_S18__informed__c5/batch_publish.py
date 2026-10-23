import os
import json
from concurrent import futures
from messaging_client import MessagingClient
from messaging_models import BatchPublishRequest, create_event_message


def publish_batch_messages(batch_request):
    batch_request.validate()

    client = MessagingClient()
    topic_path = client.get_topic_path(batch_request.topic_id)

    futures_list = []
    message_ids = []

    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        for i, event_message in enumerate(batch_request.messages):
            message_data = event_message.to_json()

            attributes = batch_request.attributes or {}
            attributes["batch_index"] = str(i)
            attributes["event_type"] = event_message.event_type
            attributes["source"] = event_message.source

            if event_message.correlation_id:
                attributes["correlation_id"] = event_message.correlation_id

            future = executor.submit(
                client.publisher_client.publish, topic_path, message_data, **attributes
            )
            futures_list.append((future, i))

        for future, index in futures_list:
            try:
                message_id = future.result(timeout=30)
                message_ids.append(
                    {
                        "index": index,
                        "message_id": message_id,
                        "event_type": batch_request.messages[index].event_type,
                    }
                )
                print(
                    f"Published batch message {index} to Google Cloud Pub/Sub topic {batch_request.topic_id}: {message_id}"
                )
            except Exception as e:
                print(
                    f"Failed to publish batch message {index} to Google Cloud Pub/Sub: {e}"
                )
                message_ids.append(
                    {
                        "index": index,
                        "error": str(e),
                        "event_type": batch_request.messages[index].event_type,
                    }
                )

    return {
        "topic_id": batch_request.topic_id,
        "total_messages": len(batch_request.messages),
        "successful": len([m for m in message_ids if "message_id" in m]),
        "failed": len([m for m in message_ids if "error" in m]),
        "results": message_ids,
    }


def create_sample_batch():
    messages = []

    for i in range(5):
        event_message = create_event_message(
            event_type=f"user_action_{i}",
            payload={
                "user_id": f"user_{1000 + i}",
                "action": ["login", "logout", "purchase", "view", "search"][i % 5],
                "timestamp": f"2024-01-{10 + i:02d}T12:00:00Z",
            },
            source="batch_processor",
            correlation_id=f"batch_corr_{i:03d}",
        )
        messages.append(event_message)

    return BatchPublishRequest(
        messages=messages,
        topic_id="user-events-batch",
        attributes={"batch_id": "batch_001", "processor": "batch_publisher"},
    )


if __name__ == "__main__":
    try:
        batch_request = create_sample_batch()
        print(
            f"Publishing batch of {len(batch_request.messages)} messages to Google Cloud Pub/Sub..."
        )

        result = publish_batch_messages(batch_request)

        print(f"\nBatch publishing completed:")
        print(f"Topic: {result['topic_id']}")
        print(f"Total: {result['total_messages']}")
        print(f"Successful: {result['successful']}")
        print(f"Failed: {result['failed']}")

        if result["failed"] > 0:
            print("\nFailed messages:")
            for msg in result["results"]:
                if "error" in msg:
                    print(
                        f"  Index {msg['index']} ({msg['event_type']}): {msg['error']}"
                    )

    except Exception as e:
        print(f"Error in batch publishing: {e}")
