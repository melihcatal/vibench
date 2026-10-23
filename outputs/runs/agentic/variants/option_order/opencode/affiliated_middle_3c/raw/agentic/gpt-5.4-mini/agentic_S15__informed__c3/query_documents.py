from database_client import get_collection


def query_documents(field_name, field_value):
    query = {field_name: field_value}
    return list(get_collection().find(query))
