from typing import List, Dict, Any

def normalize_labels_response(response: Dict[str, Any]) -> List[str]:
    labels = []
    # This is a placeholder for actual response parsing
    # The actual parsing will depend on the specific OpenAI vision model response structure
    if 'choices' in response and response['choices']:
        for choice in response['choices']:
            if 'message' in choice and 'content' in choice['message']:
                # Assuming the content is a string that might contain comma-separated labels
                # Or, it might be more structured. This is a basic attempt.
                content_text = choice['message']['content']
                # Simple heuristic: if it looks like a list or comma-separated string
                if '[' in content_text and ']' in content_text:
                    try:
                        import json
                        parsed_content = json.loads(content_text)
                        if isinstance(parsed_content, list):
                            labels.extend(parsed_content)
                    except json.JSONDecodeError:
                        labels.append(content_text.strip())
                else:
                    # Split by common delimiters if not JSON array
                    if ',' in content_text:
                        labels.extend([item.strip() for item in content_text.split(',') if item.strip()])
                    else:
                        labels.append(content_text.strip())
    return labels

def normalize_description_response(response: Dict[str, Any]) -> str:
    if 'choices' in response and response['choices']:
        for choice in response['choices']:
            if 'message' in choice and 'content' in choice['message']:
                return choice['message']['content'].strip()
    return ""

def normalize_text_detection_response(response: Dict[str, Any]) -> List[str]:
    texts = []
    if 'text_annotations' in response:
        for text in response['text_annotations']:
            if 'description' in text:
                texts.append(text['description'])
    # The first text annotation is usually the full detected text
    if texts:
        return [texts[0]] # Return the full text as a list with one element
    return []

def normalize_content_moderation_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    safety_labels = []
    if 'ModerationLabels' in response:
        for label in response['ModerationLabels']:
            safety_labels.append({
                'Name': label['Name'],
                'Confidence': label['Confidence'],
                'ParentName': label.get('ParentName', None)
            })
    return safety_labels

def normalize_translation_response(response: Dict[str, Any]) -> str:
    if 'translations' in response and response['translations']:
        return response['translations'][0]['translated_text']
    return ""

def normalize_comprehend_safety_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    toxic_content = []
    if 'ResultList' in response:
        for result in response['ResultList']:
            if 'Labels' in result:
                for label in result['Labels']:
                    toxic_content.append({
                        'Name': label['Name'],
                        'Score': label['Score'],
                        'Violence': label['Violence'] if 'Violence' in label else None,
                        'Graphic': label['Graphic'] if 'Graphic' in label else None,
                        'Hate': label['Hate'] if 'Hate' in label else None,
                        'Sexual': label['Sexual'] if 'Sexual' in label else None,
                        'Harassment': label['Harassment'] if 'Harassment' in label else None,
                    })
    return toxic_content



