from google.cloud import pubsub_v1
import os
import time

def process_message_with_potential_failure(project_id: str, subscription_id: str, max_attempts: int = 3):
    """Simulates message processing with potential failure and nacking, leading to dead-letter queue if configured.
    Assumes the subscription is already configured with a Dead Letter Topic and max_delivery_attempts.
    """
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message):
        print(f"Received message: {message.data.decode('utf-8')}")
        try:
            # Simulate a processing failure
            if "fail" in message.data.decode('utf-8').lower():
                raise ValueError("Simulated processing error!")
            
            print("Message processed successfully. Acknowledging.")
            message.ack()
        except Exception as e:
            print(f"Processing failed for message ID {message.message_id}: {e}. Nacking message.")
            message.nack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path} (configured with DLQ if applicable)...")

    # Keep the subscriber alive for a short period to demonstrate
    try:
        streaming_pull_future.result(timeout=30)  # Listen for 30 seconds
    except TimeoutError:
        print("No messages received or timed out.")
        streaming_pull_future.cancel()
        streaming_pull_future.result()  # Reraises the exception to show cancellation
    except Exception as e:
        print(f"An error occurred during subscription: {e}")
        streaming_pull_future.cancel()
        streaming_pull_future.result()
    finally:
        subscriber.api.transport.close()

if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    subscription_id = os.getenv("GOOGLE_CLOUD_PUBSUB_SUBSCRIPTION_ID_DLQ")

    if not all([project_id, subscription_id]):
        print("Please set GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_PUBSUB_SUBSCRIPTION_ID_DLQ environment variables.")
        print("Ensure the subscription is configured with a dead-letter topic and max_delivery_attempts.")
    else:
        process_message_with_potential_failure(project_id, subscription_id)
