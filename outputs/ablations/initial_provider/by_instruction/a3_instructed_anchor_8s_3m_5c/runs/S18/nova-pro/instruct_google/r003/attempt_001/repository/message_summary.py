def summarize_messages(messages):
    return {'total': len(messages), 'data': [message.data for message in messages]}