from google.cloud import documentai

# Initialize the client
client = documentai.DocumentProcessorServiceClient()


def extract_layout(document_path):
    with open(document_path, "rb") as document_file:
        document = documentai.Document(content=document_file.read())
        response = client.process_document(document)
        return response.entities
