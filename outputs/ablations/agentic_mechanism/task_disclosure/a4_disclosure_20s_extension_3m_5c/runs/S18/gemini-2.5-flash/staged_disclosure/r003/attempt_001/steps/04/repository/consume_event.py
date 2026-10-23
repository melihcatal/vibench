import os
from google.cloud import pubsub_v1

# Ensure you have authenticated to Google Cloud.
# For example, by running `gcloud auth application-default login`
# or setting the GOOGLE_APPLICATION_CREDENTIALS environment variable.

project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
subscription_id = os.environ.get("PUBSUB_SUBSCRIPTION_ID")

if not project_id:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")
if not subscription_id:
    raise ValueError("PUBSUB_SUBSCRIPTION_ID environment variable must be set.")

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

print(f"Listening for one message on {subscription_path}...")

# The subscriber pulls one message at a time.
# Setting max_messages to 1 to ensure only one message is pulled.
# Timeout of 5 seconds for the pull request.
try:
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1},
        retry=None,
        timeout=5.0,
    )

    if response.received_messages:
        for received_message in response.received_messages:
            message = received_message.message
            print(f"Received message: {message.data.decode('utf-8')}")
            
            # Acknowledge the message to remove it from the subscription.
            ack_ids = [received_message.ack_id]
            subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": ack_ids})
            print(f"Acknowledged message: {received_message.ack_id}")
            break # Process only the first message
    else:
        print("No messages received within the timeout period.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    subscriber.close()
