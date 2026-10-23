def normalize_event(event):
    return event.encode('utf-8')

def parse_message(message):
    return message.data.decode('utf-8')