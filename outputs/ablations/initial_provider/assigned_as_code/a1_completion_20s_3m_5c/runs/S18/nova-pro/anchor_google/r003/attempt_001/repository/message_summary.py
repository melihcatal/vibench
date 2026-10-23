import json


def summarize_message_processing(messages):
    summary = {'total_messages': len(messages), 'message_ids': [message['message_id'] for message in messages]}
    return json.dumps(summary)