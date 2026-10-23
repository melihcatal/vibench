def summarize_message_processing(messages):
    summary = {
        'total_messages': len(messages),
        'success_count': 0,
        'failure_count': 0
    }
    for message in messages:
        if message.get('status') == 'success':
            summary['success_count'] += 1
        else:
            summary['failure_count'] += 1
    return summary