def static_image_request(image_path: str) -> dict:
    return {
        'image_path': image_path,
        'model': 'amazon-nova-api/nova-pro-v1'
    }


def visual_understanding_request(image_path: str, query: str) -> dict:
    return {
        'image_path': image_path,
        'query': query,
        'model': 'amazon-nova-api/nova-pro-v1'
    }


def normalize_response(response: dict) -> dict:
    return {
        'normalized_data': response.get('data', {})
    }
