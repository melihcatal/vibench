import json
from typing import Dict, Any, List

def parse_textract_expense(response: Dict[str, Any]) -> Dict[str, Any]:
    if 'ExpenseDocuments' not in response or not response['ExpenseDocuments']:
        return {'error': 'No expense documents found'}
    
    doc = response['ExpenseDocuments'][0]
    fields: Dict[str, Dict[str, Any]] = {}
    
    if 'SummaryPages' in doc and doc['SummaryPages']:
        summary = doc['SummaryPages'][0]
        for field in summary.get('LineItemExpenseFields', []):
            type_key = field['Type']['Text']
            fields[type_key] = {
                'text': field['Text'],
                'confidence': field['Confidence']
            }
    
    line_items: List[Dict[str, Any]] = []
    if 'LineItemExpenseGroups' in doc:
        for group in doc['LineItemExpenseGroups']:
            item: Dict[str, Dict[str, Any]] = {}
            for field in group.get('LineItemExpenseFields', []):
                type_key = field['Type']['Text']
                item[type_key] = {
                    'text': field['Text'],
                    'confidence': field['Confidence']
                }
            line_items.append(item)
    
    fields['line_items'] = line_items
    return fields
