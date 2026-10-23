import boto3

def validate_document_fields(document):
    comprehend = boto3.client('comprehend')
    try:
        response = comprehend.detect_entities(Text=document, LanguageCode='en')
        entities = response['Entities']
        required_fields = ['VENDOR', 'DATE', 'TOTAL']
        field_scores = {}
        for entity in entities:
            if entity['Type'] in required_fields:
                field_scores[entity['Type']] = entity['Score']
        for field in required_fields:
            if field not in field_scores or field_scores[field] < 0.5:
                return False, f'Missing or low confidence score for {field}'
        return True, 'All required fields validated successfully'
    except Exception as e:
        return False, str(e)