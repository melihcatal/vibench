from botocore.exceptions import ClientError


class VisionModel:
    def __init__(self, rekognition_client):
        self.rekognition_client = rekognition_client

    def normalize_response(self, response):
        normalized_response = {}
        for key, value in response.items():
            if isinstance(value, list):
                normalized_response[key] = [self._normalize_item(item) for item in value]
            else:
                normalized_response[key] = self._normalize_item(value)
        return normalized_response

    def _normalize_item(self, item):
        if isinstance(item, dict):
            return {k: self._normalize_item(v) for k, v in item.items()}
        return item

    def handle_request(self, request_type, **kwargs):
        try:
            response = getattr(self.rekognition_client, request_type)(**kwargs)
            return self.normalize_response(response)
        except ClientError as e:
            print(f"Error: {e}")
            return None

