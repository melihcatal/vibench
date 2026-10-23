import mindee


def extract_tables(image_path):
    client = mindee.Client(api_key=os.getenv("MINDEE_API_KEY"))
    document = client.documents.upload(image_path)
    result = document.parse()
    return result.tables
