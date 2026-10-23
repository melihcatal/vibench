from storage_client import upload_to_storage

def record_export_archive(document, file_path):
    return upload_to_storage(file_path, 'exported-documents')