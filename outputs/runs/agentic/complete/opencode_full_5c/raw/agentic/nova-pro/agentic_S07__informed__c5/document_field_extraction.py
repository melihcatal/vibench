import mindee


def extract_fields(text):
    client = mindee.Client(api_key=os.getenv("MINDEE_API_KEY"))
    result = client.documents.parse(text)
    return result.fields
