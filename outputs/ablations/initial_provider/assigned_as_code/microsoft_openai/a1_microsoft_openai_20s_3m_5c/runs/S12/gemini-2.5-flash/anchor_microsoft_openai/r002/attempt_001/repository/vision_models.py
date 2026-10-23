from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ImageAnalysisRequest:
    image_bytes: bytes
    visual_features: List[Any]

@dataclass
class ImageAnalysisResponse:
    result: Dict[str, Any]

def normalize_tags_response(tags_result, max_labels=10):
    if not tags_result or not tags_result.tags:
        return []
    tags = sorted(tags_result.tags.list, key=lambda tag: tag.confidence, reverse=True)
    return [{'name': tag.name, 'confidence': tag.confidence}
            for tag in tags[:int(max_labels)]]

def normalize_caption_response(caption_result):
    if not caption_result or not caption_result.caption:
        return None
    return {'text': caption_result.caption.content, 'confidence': caption_result.caption.confidence}

def normalize_dense_caption_response(dense_caption_result, max_captions=5):
    if not dense_caption_result or not dense_caption_result.dense_captions:
        return []
    captions = sorted(dense_caption_result.dense_captions.list, key=lambda caption: caption.confidence, reverse=True)
    return [{'text': caption.content, 'confidence': caption.confidence, 'bounding_box': 
             {'x': caption.bounding_box.x, 'y': caption.bounding_box.y, 
              'w': caption.bounding_box.w, 'h': caption.bounding_box.h}}
            for caption in captions[:int(max_captions)]]

def normalize_text_response(text_result):
    if not text_result or not text_result.text:
        return []
    
    extracted_text = []
    for line in text_result.text.lines:
        words_data = []
        for word in line.words:
            words_data.append({'text': word.content, 'confidence': word.confidence})
        extracted_text.append({'content': line.content, 'bounding_box': 
                               {'x': line.bounding_box[0], 'y': line.bounding_box[1], 
                                'w': line.bounding_box[2] - line.bounding_box[0], 
                                'h': line.bounding_box[7] - line.bounding_box[1]}, 
                               'words': words_data})
    return extracted_text

def normalize_general_object_response(objects_result, max_objects=10):
    if not objects_result or not objects_result.objects:
        return []
    objects = sorted(objects_result.objects.list, key=lambda obj: obj.confidence, reverse=True)
    return [{'name': obj.tags[0].name if obj.tags else None, 'confidence': obj.confidence, 
             'bounding_box': {'x': obj.bounding_box.x, 'y': obj.bounding_box.y, 
                              'w': obj.bounding_box.w, 'h': obj.bounding_box.h}}
            for obj in objects[:int(max_objects)]]

def normalize_image_quality_response(image_quality_result):
    if not image_quality_result or not image_quality_result.image_quality:
        return None
    return {
        'brightness': image_quality_result.image_quality.brightness,
        'contrast': image_quality_result.image_quality.contrast
    }

def normalize_people_response(people_result):
    if not people_result or not people_result.people:
        return []
    people = sorted(people_result.people.list, key=lambda person: person.confidence, reverse=True)
    return [{'confidence': person.confidence,
             'bounding_box': {'x': person.bounding_box.x, 'y': person.bounding_box.y,
                              'w': person.bounding_box.w, 'h': person.bounding_box.h}}
            for person in people]

def normalize_redaction_response(redaction_result):
    if not redaction_result or not redaction_result.redaction:
        return None
    return {'status': redaction_result.redaction.status.value}

def normalize_face_response(face_result):
    if not face_result or not face_result.faces:
        return []
    return [{'age': face.age, 'bounding_box': {'x': face.bounding_box.x, 'y': face.bounding_box.y,
                                               'w': face.bounding_box.w, 'h': face.bounding_box.h},
             'gender': face.gender.value}
            for face in face_result.faces.list]

def normalize_crop_suggestion_response(crop_result):
    if not crop_result or not crop_result.smart_crops:
        return []
    return [{'bounding_box': {'x': crop.bounding_box.x, 'y': crop.bounding_box.y,
                                'w': crop.bounding_box.w, 'h': crop.bounding_box.h}}
            for crop in crop_result.smart_crops.list]

def normalize_color_response(color_result):
    if not color_result or not color_result.color:
        return None
    return {
        'accent_color': color_result.color.accent_color,
        'dominant_background': color_result.color.dominant_background,
        'dominant_foreground': color_result.color.dominant_foreground,
        'dominant_colors': [c.value for c in color_result.color.dominant_colors],
        'is_b_w': color_result.color.is_b_w_image
    }

def normalize_replicate_model_response(result):
    # This is a placeholder for a generic replicate model response normalization
    # The actual structure would depend on the specific replicate model used.
    return result
