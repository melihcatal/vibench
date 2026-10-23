def validate_document_fields(fields):
    required_fields = ['vendor', 'date', 'total']
    for field in required_fields:
        if field not in fields or not fields[field]:
            raise ValueError(f'{field} is missing or empty')
    if 'confidence' in fields and fields['confidence'] < 0.5:
        raise ValueError('Confidence score is too low')