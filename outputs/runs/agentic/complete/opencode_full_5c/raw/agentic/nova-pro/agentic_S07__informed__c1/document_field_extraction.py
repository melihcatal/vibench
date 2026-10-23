import mindee


def extract_fields(document_path):
    client = mindee.Client(api_key=os.getenv("MINDEE_API_KEY"))
    document = client.document_from_path(document_path)
    response = client.parse(document)
    return response
