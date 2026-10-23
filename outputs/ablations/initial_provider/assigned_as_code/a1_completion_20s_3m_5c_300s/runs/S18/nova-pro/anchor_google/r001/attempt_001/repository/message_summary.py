from messaging_models import Message

def message_summary(messages):
    return [{"message_id": message.message_id, "payload": message.payload} for message in messages]