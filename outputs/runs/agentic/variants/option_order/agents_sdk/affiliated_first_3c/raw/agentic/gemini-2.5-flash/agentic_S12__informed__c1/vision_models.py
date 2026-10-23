from typing import List, Dict, Any, Optional

# A simple type alias for image content, which is typically bytes.
ImageContent = bytes

# Define simple structures for normalized results, if needed.
# In this example, the direct output from vision API calls is used in scored files,
# but these classes could be used to standardize outputs across different vision providers
# or for internal data passing.

class ImageLabel:
    def __init__(self, description: str, score: float):
        self.description = description
        self.score = score

    def to_dict(self):
        return {"description": self.description, "score": self.score}

class ImageText:
    def __init__(self, text: str, locale: Optional[str] = None):
        self.text = text
        self.locale = locale

    def to_dict(self):
        return {"text": self.text, "locale": self.locale}

class ImageSafetyScore:
    def __init__(self, category: str, likelihood: str):
        self.category = category
        self.likelihood = likelihood

    def to_dict(self):
        return {"category": self.category, "likelihood": self.likelihood}

class ImageAnalysisResult:
    """A composite result structure for image analysis."""
    def __init__(
        self,
        labels: Optional[List[ImageLabel]] = None,
        description: Optional[str] = None,
        text_content: Optional[ImageText] = None,
        safety_scores: Optional[List[ImageSafetyScore]] = None,
    ):
        self.labels = labels if labels is not None else []
        self.description = description
        self.text_content = text_content
        self.safety_scores = safety_scores if safety_scores is not None else []

    def to_dict(self):
        return {
            "labels": [label.to_dict() for label in self.labels],
            "description": self.description,
            "text_content": self.text_content.to_dict() if self.text_content else None,
            "safety_scores": [score.to_dict() for score in self.safety_scores],
        }

if __name__ == '__main__':
    print("Running vision_models.py example...")
    label1 = ImageLabel("cat", 0.95)
    label2 = ImageLabel("animal", 0.90)
    text_data = ImageText("Hello World")
    safety1 = ImageSafetyScore("violence", "VERY_UNLIKELY")

    result = ImageAnalysisResult(
        labels=[label1, label2],
        description="A furry feline",
        text_content=text_data,
        safety_scores=[safety1]
    )
    print(result.to_dict())
