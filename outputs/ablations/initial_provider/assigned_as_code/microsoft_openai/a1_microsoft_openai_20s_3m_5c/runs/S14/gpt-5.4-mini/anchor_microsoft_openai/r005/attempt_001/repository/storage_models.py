def normalize_config(config=None):
    return dict(config or {})


def normalize_payload(payload=None):
    return dict(payload or {})


def object_name_from(payload):
    return payload['object_name']


def object_response(name, **extra):
    data = {'object_name': name}
    data.update(extra)
    return data
