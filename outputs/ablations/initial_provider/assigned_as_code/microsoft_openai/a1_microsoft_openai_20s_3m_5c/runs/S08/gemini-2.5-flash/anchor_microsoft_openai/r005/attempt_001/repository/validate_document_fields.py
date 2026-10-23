import os
import requests
from typing import Dict, Any

def validate_document_fields(extracted_fields: Dict[str, Any], document_type: str, config=None) -> Dict[str, Any]:
    config = config or {}
    validation_results = {'is_valid': True, 'errors': [], 'warnings': [], 'moderation_results': []}

    # Basic structural validation (local)
    if document_type == 'invoice':
        required_fields = ['vendor', 'date', 'total']
    elif document_type == 'receipt':
        required_fields = ['merchant', 'total', 'tax']
    else:
        validation_results['is_valid'] = False
        validation_results['errors'].append(f"Unsupported document type: {document_type}")
        return validation_results

    for field in required_fields:
        if not extracted_fields.get(field):
            validation_results['is_valid'] = False
            validation_results['errors'].append(f"Missing required field: {field}")

    # Scored component: Use Azure Content Moderator for text safety on vendor name/merchant name
    text_to_moderate = None
    if document_type == 'invoice':
        text_to_moderate = extracted_fields.get('vendor')
    elif document_type == 'receipt':
        text_to_moderate = extracted_fields.get('merchant')

    if text_to_moderate and config.get('content_moderator_endpoint') and config.get('content_moderator_subscription_key'):
        endpoint = config['content_moderator_endpoint']
        subscription_key = config['content_moderator_subscription_key']
        url = f"{endpoint}/contentmoderator/moderate/v1.0/ProcessText/Screen?classify=True"
        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Content-Type': 'text/plain',
        }
        try:
            response = requests.post(url, headers=headers, data=text_to_moderate)
            response.raise_for_status()
            moderation_data = response.json()
            validation_results['moderation_results'].append({'field': 'vendor_or_merchant_name', 'data': moderation_data})
            if moderation_data.get('Classification') and moderation_data['Classification'].get('ReviewRecommended'):
                validation_results['is_valid'] = False
                validation_results['warnings'].append("Content moderation review recommended for vendor/merchant name.")
        except requests.exceptions.RequestException as e:
            validation_results['warnings'].append(f"Content Moderator API error: {e}")

    return validation_results
