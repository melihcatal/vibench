from messaging_client import get_publisher_client, get_subscriber_client, get_project_id
import time
import json

def process_message_with_dead_letter(subscription_id: str, dead_letter_topic_id: str):
    project_id = get_project_id()
    subscriber = get_subscriber_client()
    publisher = get_publisher_client()

    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    def callback(message):
        try:
            payload = message.data.decode("utf-8")
            print(f"Attempting to process message: {payload}")
            # Simulate a processing failure
            if "fail_me" in payload:
                raise ValueError("Simulated processing failure")
            
            print(f"Successfully processed message: {payload}")
            message.ack()
        except Exception as e:
            print(f"Message processing failed: {e}. Sending to dead-letter topic.")
            error_payload = {
                "original_message": payload,
                "error": str(e),
                "timestamp": time.time()
            }
            publisher.publish(dead_letter_topic_path, json.dumps(error_payload).encode("utf-8"))
            message.ack() # Acknowledge the original message after sending to DLQ

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path} with dead-lettering to {dead_letter_topic_id}. Press Ctrl+C to exit.")

    with subscriber:
        try:
            streaming_pull_future.result(timeout=60)
        except Exception as ex:
            streaming_pull_future.cancel()
            streaming_pull_future.result()
            raise ex


if __name__ == "__main__":
    # Example usage (replace with your subscription_id and dead_letter_topic_id)
    example_subscription_id = "your-subscription-id"
    example_dead_letter_topic_id = "your-dead-letter-topic-id"
    process_message_with_dead_letter(example_subscription_id, example_dead_letter_topic_id)
