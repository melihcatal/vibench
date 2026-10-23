import os
from google.cloud import documentai_v1 as documentai

# Use Document AI Table parser (extracts tables from document images)
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us"
PROCESSOR_ID = "projects/{}/locations/{}/processors/{}".format(PROJECT_ID, LOCATION, "document-table-parser")

def extract_tables_from_image(image_bytes):
    client = documentai.DocumentProcessorServiceClient()
    raw_document = documentai.RawDocument(content=image_bytes, mime_type="image/png")
    input_config = documentai.InputConfig(raw_document=raw_document)
    request = documentai.ProcessRequest(name=PROCESSOR_ID, input_config=input_config)
    result = client.process_document(request=request)
    # Convert table annotations to cell data
    tables = []
    for entity in result.document.entities:
        if entity.type_ == "TABLE":
            rows = []
            for row in entity.table.rows:
                cells = [cell.text for cell in row.cells]
                rows.append(cells)
            tables.append({"header": entity.table.header, "rows": rows})
    return tables
