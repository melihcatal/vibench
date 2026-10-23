import os
from openai import OpenAI
from typing import Dict, Any, List

def check_record_safety(record: Dict[str, Any]) -> Dict[str, bool]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    # Assume checking 'content' and 'text' fields
    fields_to_check = ['content', 'text', 'description']
    safety_results = {}
    
    for field in fields_to_check:
        if field in record and isinstance(record[field], str):
            text = record[field]
            response = client.moderations.create(input=text)
            flagged = response.results[0].flagged
            safety_results[field] = not flagged
    
    return safety_results