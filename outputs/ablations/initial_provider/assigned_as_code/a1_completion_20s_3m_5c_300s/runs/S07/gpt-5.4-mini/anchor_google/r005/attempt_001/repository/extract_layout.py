from google.cloud import documentai

from document_client import normalize_config, make_documentai_client
from document_models import normalize_layout_blocks


def extract_layout(payload, config=None):
    config = normalize_config(config)
    client = make_documentai_client(config["location"])
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(request={"name": name, "raw_document": documentai.RawDocument(content=payload["document_bytes"], mime_type=payload["mime_type"])})
    document = response.document
    blocks = []
    for page in document.pages:
        for block in page.blocks:
            blocks.append({"text": block.layout.text_anchor.content if hasattr(block.layout.text_anchor, "content") else ""})
        for table in page.tables:
            blocks.append({"rows": len(table.header_rows) + len(table.body_rows), "type": "table"})
        for line in page.lines:
            blocks.append({"text": line.layout.text_anchor.content if hasattr(line.layout.text_anchor, "content") else "", "type": "line"})
    return {"layout": normalize_layout_blocks(blocks)}
