def normalize_email(email):
    return (email or '').strip().lower()


def normalize_locale(locale):
    return (locale or 'en').strip().replace('_', '-').lower()


def build_email_password_payload(payload):
    payload = payload or {}
    return {
        'email': normalize_email(payload.get('email')),
        'password': payload.get('password', ''),
    }


def build_locale_payload(payload):
    payload = payload or {}
    return {
        'text': payload.get('text', ''),
        'locale': normalize_locale(payload.get('locale')),
    }


def build_support_payload(payload):
    payload = payload or {}
    return {
        'user_id': payload.get('user_id', ''),
        'email': normalize_email(payload.get('email')),
        'status': payload.get('status', ''),
    }
