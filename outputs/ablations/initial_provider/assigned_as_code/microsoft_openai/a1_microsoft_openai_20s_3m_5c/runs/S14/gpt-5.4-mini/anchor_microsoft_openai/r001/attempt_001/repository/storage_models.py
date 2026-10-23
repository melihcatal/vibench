def normalize_object_name(value):
    if value is None:
        return ''
    return str(value).lstrip('/')


def normalize_prefix(value):
    if value is None:
        return ''
    prefix = str(value)
    return prefix if prefix.endswith('/') or prefix == '' else prefix


def metadata_to_dict(metadata, name=None):
    data = dict(metadata or {})
    if name is not None:
        data['object_name'] = normalize_object_name(name)
    return data
