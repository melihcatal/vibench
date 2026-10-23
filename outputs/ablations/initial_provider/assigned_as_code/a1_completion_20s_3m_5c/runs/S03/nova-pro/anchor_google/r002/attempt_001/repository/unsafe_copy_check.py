from google.cloud import translate_v3

from translation_client import get_translation_client


def check_unsafe_copy(translations, config=None):
    config = config or {}
    client = get_translation_client(config)
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    response = client.check_translation_safety(request={
        "parent": parent,
        "translations": translations,
   })
    unsafe_copy = []
    for check in response.checks:
        if check.is_unsafe:
            unsafe_copy.append({
                "text": check.text,
                "reason": check.reason,
           })
    return unsafe_copy