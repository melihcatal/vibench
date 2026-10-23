def normalize_request(payload):
    return {'text': payload['text']}



def normalize_response(response):
    return {'text': response.choices[0].message.content}