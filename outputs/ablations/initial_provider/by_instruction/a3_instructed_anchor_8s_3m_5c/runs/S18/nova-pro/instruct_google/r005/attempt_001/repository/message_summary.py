def summarize_messages(messages):
    summary = {
        'total_messages': len(messages),
        'message_types': {}
    }
    for message in messages:
        message_type = message.get('event_type')
        if message_type in summary['message_types']:
            summary['message_types'][message_type] += 1
        else:
            summary['message_types'][message_type] = 1
    return summary