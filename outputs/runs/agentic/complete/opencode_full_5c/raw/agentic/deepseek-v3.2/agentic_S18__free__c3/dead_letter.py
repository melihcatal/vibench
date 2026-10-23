import os
import json
from google.cloud import pubsub_v1


def send_to_dead_letter(message_data, error_reason, dead_letter_topic_id=None):
    """Sends failed messages to a dead-letter destination."""
    if dead_letter_topic_id is None:
        dead_letter_topic_id = os.environ.get(
            "PUBSUB_DEAD_LETTER_TOPIC_ID",
            "projects/my-project/topics/dead-letter-topic",
        )

    publisher = pubsub_v1.PublisherClient()

    # Create dead letter message with original data and error info
    dead_letter_message = {
        "original_message": message_data,
        "error_reason": error_reason,
        "timestamp": "2023-10-01T12:00:00Z",
        "source": "message_processor",
    }

    data = json.dumps(dead_letter_message).encode("utf-8")

    # Add attributes to identify as dead letter
    future = publisher.publish(
        dead_letter_topic_id,
        data,
        message_type="dead_letter",
        error_reason=error_reason[:100],  # Limit attribute length
    )

    message_id = future.result()

    return {
        "message_id": message_id,
        "dead_letter_topic": dead_letter_topic_id,
        "error_reason": error_reason,
    }


def process_with_dead_letter(message_data, processing_function):
    """Process a message with dead letter handling."""
    try:
        result = processing_function(message_data)
        return {"success": True, "result": result}
    except Exception as e:
        error_reason = str(e)
        dead_letter_result = send_to_dead_letter(message_data, error_reason)
        return {
            "success": False,
            "error": error_reason,
            "dead_letter_info": dead_letter_result,
        }


if __name__ == "__main__":
    # Example processing function that might fail
    def example_processor(data):
        if "test" in data:
            raise ValueError("Test message should fail")
        return {"processed": True, "data": data}

    # Test with a failing message
    test_message = {"content": "test message", "id": "123"}
    result = process_with_dead_letter(test_message, example_processor)
    print(f"Processing result: {result}")
