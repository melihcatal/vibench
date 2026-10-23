def summarize_message_processing(messages):
    total_messages = len(messages)
    successful_messages = sum(1 for msg in messages if msg.get('status') == 'success')
    failed_messages = total_messages - successful_messages
    return {
        'total_messages': total_messages,
        'successful_messages': successful_messages,
        'failed_messages': failed_messages
    }