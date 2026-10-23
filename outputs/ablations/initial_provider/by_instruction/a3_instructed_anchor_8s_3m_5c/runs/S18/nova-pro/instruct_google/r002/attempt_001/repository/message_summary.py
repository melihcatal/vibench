def summarize_messages(messages):
    summary = {'total': len(messages), 'data': []}
    for message in messages:
        summary['data'].append(message.to_dict())
    return summary