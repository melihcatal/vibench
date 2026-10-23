def normalize_email(email):
    return email.strip().lower()


def build_user_payload(email, password, display_name=None, locale=None):
    payload = {'email': normalize_email(email), 'password': password}
    if display_name is not None:
        payload['displayName'] = display_name
    if locale is not None:
        payload['locale'] = locale
    return payload


def parse_tokens(token_response):
    return {
        'access_token': token_response.get('access_token'),
        'refresh_token': token_response.get('refresh_token'),
        'id_token': token_response.get('id_token'),
        'expires_in': token_response.get('expires_in'),
        'token_type': token_response.get('token_type'),
    }


def build_support_note(email, status, metadata=None):
    return {
        'email': normalize_email(email),
        'status': status,
        'metadata': metadata or {},
    }
