def summarize_message_processing(messages):
    return {'total_messages': len(messages), 'first_message': messages[0] if messages else None}