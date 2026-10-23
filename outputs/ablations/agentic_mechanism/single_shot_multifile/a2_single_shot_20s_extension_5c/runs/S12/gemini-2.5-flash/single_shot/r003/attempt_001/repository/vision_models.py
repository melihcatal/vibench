import base64

def prepare_image_for_aws(image_bytes: bytes):
    return {'Bytes': image_bytes}

def prepare_image_for_google(image_bytes: bytes):
    return {'content': image_bytes}

def prepare_image_for_azure_vision(image_bytes: bytes):
    return image_bytes

def parse_aws_rekognition_labels(response):
    labels = []
    for label in response.get('Labels', []):
        labels.append({
            'name': label.get('Name'),
            'confidence': label.get('Confidence')
        })
    return {'labels': labels}

def parse_google_vision_text_detection(response):
    texts = []
    if response.full_text_annotation:
        texts.append({'full_text': response.full_text_annotation.text})
    for i, text_annotation in enumerate(response.text_annotations):
        if i == 0 and response.full_text_annotation and text_annotation.description == response.full_text_annotation.text:
            continue
        texts.append({
            'description': text_annotation.description,
            'bounding_poly': [{'x': v.x, 'y': v.y} for v in text_annotation.bounding_poly.vertices]
        })
    return {'detected_texts': texts}

def parse_azure_caption_result(analysis_result):
    if analysis_result and analysis_result.caption:
        return {'description': analysis_result.caption.content, 'confidence': analysis_result.caption.confidence}
    return {'description': None, 'confidence': 0.0}

def parse_azure_content_safety_result(analyze_image_result):
    categories = {}
    if analyze_image_result.categories_analysis:
        for category in analyze_image_result.categories_analysis:
            categories[category.category.name.lower()] = {
                'severity': category.severity,
                'detected': category.detected
            }
    return {'safety_scores': categories}

def parse_openai_summary(response):
    if response.choices and response.choices[0].message:
        return {'summary': response.choices[0].message.content}
    return {'summary': None}

def parse_google_translate_result(response):
    if response.translations:
        return {'translated_text': response.translations[0].translated_text}
    return {'translated_text': None}

def parse_openai_moderation_result(response):
    results = []
    for result in response.results:
        categories = {
            'harassment': result.categories.harassment,
            'harassment_threatening': result.categories.harassment_threatening,
            'hate': result.categories.hate,
            'hate_threatening': result.categories.hate_threatening,
            'self_harm': result.categories.self_harm,
            'self_harm_intent': result.categories.self_harm_intent,
            'self_harm_instructions': result.categories.self_harm_instructions,
            'sexual': result.categories.sexual,
            'sexual_minors': result.categories.sexual_minors,
            'violence': result.categories.violence,
            'violence_graphic': result.categories.violence_graphic,
        }
        scores = {
            'harassment': result.category_scores.harassment,
            'harassment_threatening': result.category_scores.harassment_threatening,
            'hate': result.category_scores.hate,
            'hate_threatening': result.category_scores.hate_threatening,
            'self_harm': result.category_scores.self_harm,
            'self_harm_intent': result.category_scores.self_harm_intent,
            'self_harm_instructions': result.category_scores.self_harm_instructions,
            'sexual': result.category_scores.sexual,
            'sexual_minors': result.category_scores.sexual_minors,
            'violence': result.category_scores.violence,
            'violence_graphic': result.category_scores.violence_graphic,
        }
        results.append({
            'flagged': result.flagged,
            'categories': categories,
            'category_scores': scores
        })
    return {'moderation_results': results}
