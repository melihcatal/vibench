import json
import boto3

def summarize_message_processing(message_processing_results):
    total_messages = len(message_processing_results)
    successful_messages = sum(1 for result in message_processing_results if result['status'] == 'success')
    failed_messages = total_messages - successful_messages
    summary = {
        'total_messages': total_messages,
        'successful_messages': successful_messages,
        'failed_messages': failed_messages
    }
    return json.dumps(summary)