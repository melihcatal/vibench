def value_content(fields, key):
    return fields[key].content if key in fields else None


def confidence_of(fields, key):
    return fields[key].confidence if key in fields and hasattr(fields[key], 'confidence') else None


def normalize_line_item(fields):
    return {
        'description': value_content(fields, 'Description'),
        'quantity': value_content(fields, 'Quantity'),
        'amount': value_content(fields, 'Amount'),
    }


def normalize_document_fields(document):
    fields = document.fields or {}
    return {
        'vendor': value_content(fields, 'VendorName'),
        'date': value_content(fields, 'InvoiceDate'),
        'total': value_content(fields, 'InvoiceTotal'),
        'confidence': {k: confidence_of(fields, k) for k in fields},
    }
