from.vision_client import get_vision_client

def image_summary(image_path):
    client = get_vision_client()
    with open(image_path, "rb") as image_data:
        result = client.analyze(image_data, features=['objects', 'caption', 'read', 'adult'])
        summary = {
            'labels': result.objects.objects,
            'description': result.caption.text,
            'text': result.read.text,
            'safety': result.adult.is_adult_content
        }
        return summary
