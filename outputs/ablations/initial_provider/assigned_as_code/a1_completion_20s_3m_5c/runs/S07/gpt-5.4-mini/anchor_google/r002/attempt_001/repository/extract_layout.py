from google.cloud import documentai

from document_client import load_config, make_client, processor_name, raw_document
from document_models import normalize_blocks


def extract_layout(payload, config=None):
    config = load_config(config)
    client = make_client(config)
    name = processor_name(client, config)
    response = client.process_document(request={"name": name, "raw_document": raw_document(payload)})
    blocks = []
    for page in response.document.pages:
        for block in page.blocks:
            blocks.append({"text": block.layout.text_anchor.content if block.layout.text_anchor else "", "type": "block", "confidence": block.layout.confidence})
        for line in page.lines:
            blocks.append({"text": line.layout.text_anchor.content if line.layout.text_anchor else "", "type": "line", "confidence": line.layout.confidence})
    return {"blocks": normalize_blocks(blocks)}
