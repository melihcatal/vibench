def normalize_item(item):
    return {k: {'S': v} for k, v in item.items()}

def deserialize_item(item):
    return {k: v['S'] for k, v in item.items()}