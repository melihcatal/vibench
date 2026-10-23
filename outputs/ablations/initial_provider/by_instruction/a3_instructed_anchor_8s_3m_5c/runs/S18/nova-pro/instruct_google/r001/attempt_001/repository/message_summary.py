def message_summary(messages):
    summary = {'total': len(messages), 'data': []}
    for message in messages:
        summary['data'].append(message.to_dict())
    return summary