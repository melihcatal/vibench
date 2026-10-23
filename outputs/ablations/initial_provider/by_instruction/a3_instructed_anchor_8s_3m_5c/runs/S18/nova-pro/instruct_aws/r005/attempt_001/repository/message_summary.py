def summarize_message_processing(messages):
    summary = {
        'total_messages': len(messages),
        'success_count': sum(1 for m in messages if m['status'] == 'success'),
        'failure_count': sum(1 for m in messages if m['status'] == 'failure')
    }
    return summary