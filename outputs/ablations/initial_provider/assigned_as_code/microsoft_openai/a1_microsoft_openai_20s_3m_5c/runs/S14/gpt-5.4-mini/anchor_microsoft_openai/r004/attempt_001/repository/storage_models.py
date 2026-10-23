def normalize_object_payload(payload):
    return {
        'object_name': payload.get('object_name') or payload.get('name'),
        'content_type': payload.get('content_type', 'application/octet-stream'),
        'data': payload.get('data'),
    }


def normalize_list_item(item):
    return {
        'name': getattr(item, 'name', item.get('name') if isinstance(item, dict) else None),
        'size': getattr(item, 'size', item.get('size') if isinstance(item, dict) else None),
        'last_modified': getattr(item, 'last_modified', item.get('last_modified') if isinstance(item, dict) else None),
    }
