import os
import boto3


def get_region_name():
    return os.getenv('AWS_REGION') or os.getenv('AWS_DEFAULT_REGION') or 'us-east-1'


def get_table_name():
    return os.environ['DYNAMODB_TABLE_NAME']


def get_document_id_name():
    return os.getenv('DYNAMODB_DOCUMENT_ID_NAME', 'document_id')


def get_partition_key_name():
    return os.getenv('DYNAMODB_PARTITION_KEY_NAME', get_document_id_name())


def get_query_index_name():
    return os.getenv('DYNAMODB_QUERY_INDEX_NAME')


def get_version_attribute_name():
    return os.getenv('DYNAMODB_VERSION_ATTRIBUTE_NAME', 'version')


def get_dynamodb_resource():
    return boto3.resource('dynamodb', region_name=get_region_name())
