from mindee import Client, InvoiceDocument

# Initialize the client
client = Client(api_key=os.getenv("MINDEE_API_KEY"))


def extract_key_values(document_path):
    with open(document_path, "rb") as document_file:
        document = InvoiceDocument(document_file.read())
        response = client.predict(document)
        return response.prediction.inference
