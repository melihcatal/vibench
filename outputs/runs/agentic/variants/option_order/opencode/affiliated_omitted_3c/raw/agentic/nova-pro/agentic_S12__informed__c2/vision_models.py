from azure.ai.vision.imageanalysis.models import VisualFeatures


def normalize_request(image_path, features):
    return {"image_path": image_path, "visual_features": features}


def normalize_response(result):
    return {
        "objects": result.objects.value,
        "caption": result.caption.value,
        "text": result.text.value,
        "adult": result.adult.is_adult_content,
    }
