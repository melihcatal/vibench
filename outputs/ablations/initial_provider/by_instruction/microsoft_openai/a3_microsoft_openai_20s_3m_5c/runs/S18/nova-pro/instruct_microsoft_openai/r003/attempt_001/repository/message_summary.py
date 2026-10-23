def summarize_messages(messages):
    summary = {"total_messages": len(messages), "message_bodies": []}
    for message in messages:
        summary["message_bodies"].append(message.body)
    return summary