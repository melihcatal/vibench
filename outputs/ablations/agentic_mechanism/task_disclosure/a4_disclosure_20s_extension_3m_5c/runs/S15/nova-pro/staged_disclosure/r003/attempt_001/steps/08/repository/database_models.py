from boto3 import client

class DynamoDBHelper:
    def __init__(self, table_name):
        self.dynamodb = client('dynamodb')
        self.table_name = table_name

    def create_item(self, item):
        normalized_item = self.normalize_item(item)
        response = self.dynamodb.put_item(
            TableName=self.table_name,
            Item=normalized_item
        )
        return response

    def get_item(self, key):
        response = self.dynamodb.get_item(
            TableName=self.table_name,
            Key=key
        )
        item = response.get('Item')
        if item:
            return self.denormalize_item(item)
        return None

    def normalize_item(self, item):
        normalized_item = {}
        for key, value in item.items():
            if isinstance(value, str):
                normalized_item[key] = {'S': value}
            elif isinstance(value, int):
                normalized_item[key] = {'N': str(value)}
            elif isinstance(value, list):
                normalized_item[key] = {'L': [{'S': str(v)} for v in value]}
        return normalized_item

    def denormalize_item(self, item):
        denormalized_item = {}
        for key, value in item.items():
            if 'S' in value:
                denormalized_item[key] = value['S']
            elif 'N' in value:
                denormalized_item[key] = int(value['N'])
            elif 'L' in value:
                denormalized_item[key] = [v['S'] for v in value['L']]
        return denormalized_item