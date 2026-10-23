import boto3
from botocore.exceptions import ClientError


def validate_document_fields(extracted_data, required_fields, config=None):
    config = config or {}
    client = boto3.client('comprehend', region_name=config.get('aws_region', 'us-east-1'))

    validation_results = {"is_valid": True, "missing_fields": [], "low_confidence_fields": []}

    document_text = ""
    if "invoice" in extracted_data:
        doc_data = extracted_data["invoice"][0]
        document_text = f"Vendor: {doc_data.get('vendor', '')} Date: {doc_data.get('date', '')} Total: {doc_data.get('total', '')}"
        for item in doc_data.get("line_items", []):
            document_text += f" {item.get('description', '')} {item.get('amount', '')}"
    elif "receipt" in extracted_data:
        doc_data = extracted_data["receipt"][0]
        document_text = f"Merchant: {doc_data.get('merchant', '')} Tax: {doc_data.get('tax', '')} Total: {doc_data.get('total', '')}"
        for item in doc_data.get("items", []):
            document_text += f" {item.get('description', '')} {item.get('amount', '')}"

    for field in required_fields:
        field_value = None
        if "invoice" in extracted_data and extracted_data["invoice"]:
            field_value = extracted_data["invoice"][0].get(field)
        elif "receipt" in extracted_data and extracted_data["receipt"]:
            field_value = extracted_data["receipt"][0].get(field)

        if not field_value:
            validation_results["is_valid"] = False
            validation_results["missing_fields"].append(field)
        else:
            try:
                # Use Comprehend to get confidence scores for the extracted text (conceptual)
                response = client.detect_entities(Text=str(field_value), LanguageCode='en')
                confidence = 0.0
                for entity in response['Entities']:
                    # This is a simplified example; in a real scenario, you'd match specific entity types
                    # and check their confidence.
                    if entity['Text'] == str(field_value):
                        confidence = entity['Score']
                        break
                
                # If no specific entity match, try general sentiment or key phrases
                if confidence == 0.0:
                    sentiment_response = client.detect_sentiment(Text=str(field_value), LanguageCode='en')
                    # Using mixed sentiment score as a proxy for uncertainty if no direct entity match
                    confidence = sentiment_response['SentimentScore']['Mixed']

                if confidence < config.get('min_confidence', 0.7):
                    validation_results["is_valid"] = False
                    validation_results["low_confidence_fields"].append({field: confidence})
            except ClientError as e:
                print(f"AWS Comprehend error: {e}")
                # If Comprehend fails, assume low confidence or invalid
                validation_results["is_valid"] = False
                validation_results["low_confidence_fields"].append({field: 0.0})

    return validation_results