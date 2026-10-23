from google.cloud import documentai


def invoice_note_translate(payload, config=None):
    config = config or {}
    client = documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"}
    )
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(
        request={
            "name": name,
            "raw_document": documentai.RawDocument(content=payload["document_bytes"], mime_type=payload["mime_type"]),
        }
    )
    notes = [entity.mention_text for entity in response.document.entities if entity.type_ in {"note", "description"}]
    return {"translated_notes": notes}
