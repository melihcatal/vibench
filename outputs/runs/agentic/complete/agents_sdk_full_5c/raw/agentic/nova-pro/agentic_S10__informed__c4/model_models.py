def format_request(messages):
    return [{'role': msg['role'], 'content': msg['content']} for msg in messages]

def parse_response(response):
    return [content['text'] for content in response.content]
