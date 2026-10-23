from google.cloud import logging_v2

def create_client(project_id):
    return logging_v2.Client(project=project_id)

def create_resource(type, labels):
    return logging_v2.Resource(type=type, labels=labels)