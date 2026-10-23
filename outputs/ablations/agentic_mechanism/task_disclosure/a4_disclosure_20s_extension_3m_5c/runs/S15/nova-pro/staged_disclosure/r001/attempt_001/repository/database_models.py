from boto3.dynamodb.conditions import Key, Attr


def create_item(table, item):
    response = table.put_item(Item=item)
    return response


def get_item(table, key):
    response = table.get_item(Key=key)
    return response.get('Item')


def query_items(table, key_condition_expression):
    response = table.query(KeyConditionExpression=key_condition_expression)
    return response.get('Items')


def normalize_item(item):
    normalized_item = {}
    for key, value in item.items():
        if isinstance(value, dict):
            normalized_item[key] = normalize_item(value)
        else:
            normalized_item[key] = value
    return normalized_item