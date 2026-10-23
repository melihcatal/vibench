def normalize_email(value):
    return str(value).strip().lower()


def normalize_locale(value, default='en'):
    text = str(value or '').strip()
    return text or default


def build_account_payload(email, password, **extra):
    payload = {'email': normalize_email(email), 'password': str(password)}
    payload.update(extra)
    return payload


def build_support_metadata(**extra):
    return dict(extra)
