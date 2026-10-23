import boto3
from database_models import DocumentConfig

def get_dynamodb_table(config: DocumentConfig):
    dynamodb = boto3.resource("dynamodb", region_name=config.region)
    table = dynamodb.Table(config.table_name)
    return table
