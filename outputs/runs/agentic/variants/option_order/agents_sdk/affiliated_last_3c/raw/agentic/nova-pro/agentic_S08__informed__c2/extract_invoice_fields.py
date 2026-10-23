from google.cloud import documentai

def extract_invoice_fields(file_path):
    client = documentai.DocumentProcessorServiceClient()
    # Add code to process the invoice and extract fields