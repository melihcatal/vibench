from document_models import validate_document_payload

def validate_document_fields(request):
    return validate_document_payload(request)
