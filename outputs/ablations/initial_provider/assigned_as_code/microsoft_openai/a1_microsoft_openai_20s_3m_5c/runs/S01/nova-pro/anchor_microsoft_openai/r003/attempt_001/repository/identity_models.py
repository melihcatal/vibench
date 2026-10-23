def normalize_payload(payload):
    return {
        'email': payload['email'],
        'password': payload['password']
    }

def normalize_response(response):
    return {
        'user_id': response['id']
    }
