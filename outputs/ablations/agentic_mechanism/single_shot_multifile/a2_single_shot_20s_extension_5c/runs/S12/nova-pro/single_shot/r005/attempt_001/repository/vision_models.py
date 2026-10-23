from typing import List, Dict

class ImageAnalysisResponse:
    def __init__(self, raw_response: Dict):
        self.raw_response = raw_response

    def get_objects(self) -> List[Dict]:
        return self.raw_response.get('objects', [])

    def get_caption(self) -> List[Dict]:
        return self.raw_response.get('caption', [])

    def get_text(self) -> List[Dict]:
        return self.raw_response.get('text', [])

    def get_adult(self) -> Dict:
        return self.raw_response.get('adult', {})

def normalize_response(response: Dict) -> ImageAnalysisResponse:
    return ImageAnalysisResponse(response)