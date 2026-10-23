
class ImageAnalysisRequest:
    """Represents a request for static image analysis."""
    def __init__(self, image_uri: str, features: list[str]):
        self.image_uri = image_uri
        self.features = features

class ImageAnalysisResponse:
    """Represents a response from static image analysis."""
    def __init__(self, raw_response: dict):
        self.raw_response = raw_response
        self.labels = []
        self.text_annotations = []
        self.safe_search_annotation = None
        self._normalize_response()

    def _normalize_response(self):
        """Normalizes the raw API response into a more usable format."""
        if 'labelAnnotations' in self.raw_response:
            self.labels = [label['description'] for label in self.raw_response['labelAnnotations']]
        if 'textAnnotations' in self.raw_response:
            self.text_annotations = [text['description'] for text in self.raw_response['textAnnotations']]
        if 'safeSearchAnnotation' in self.raw_response:
            self.safe_search_annotation = self.raw_response['safeSearchAnnotation']

def normalize_alt_text(description: str) -> str:
    """Normalizes generated image descriptions (alt text)."""
    # Example: Basic cleaning, could include more sophisticated NLP
    return description.strip().replace('\n', ' ').replace('  ', ' ')

def normalize_safety_score(score: dict) -> dict:
    """Normalizes safety scores from vision API responses."""
    normalized_scores = {}
    for category, likelihood in score.items():
        # Map likelihood values (e.g., 'VERY_UNLIKELY', 'LIKELY') to a numerical scale
        # This is a simplified example; real-world might use a more complex mapping
        likelihood_map = {
            'UNKNOWN': 0, 'VERY_UNLIKELY': 1, 'UNLIKELY': 2,
            'POSSIBLE': 3, 'LIKELY': 4, 'VERY_LIKELY': 5
        }
        normalized_scores[category] = likelihood_map.get(likelihood, 0)
    return normalized_scores
