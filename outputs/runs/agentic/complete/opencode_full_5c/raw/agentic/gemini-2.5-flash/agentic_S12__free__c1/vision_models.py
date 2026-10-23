import base64
from typing import List, Dict, Any


class ImageRequest:
    def __init__(self, image_content: str = None, gcs_uri: str = None):
        self.image_content = image_content  # Base64 encoded image
        self.gcs_uri = gcs_uri

    def to_dict(self):
        image_source = {}
        if self.image_content:
            image_source = {"content": self.image_content}
        elif self.gcs_uri:
            image_source = {"source": {"image_uri": self.gcs_uri}}
        return {"image": image_source}


class LabelDetectionResponse:
    def __init__(self, labels: List[Dict[str, Any]]):
        self.labels = labels

    @classmethod
    def from_vision_response(cls, response):
        labels = []
        if response.label_annotations:
            for label in response.label_annotations:
                labels.append({"description": label.description, "score": label.score})
        return cls(labels)


class TextDetectionResponse:
    def __init__(self, full_text: str, pages: List[Dict[str, Any]]):
        self.full_text = full_text
        self.pages = pages

    @classmethod
    def from_vision_response(cls, response):
        full_text = (
            response.full_text_annotation.text if response.full_text_annotation else ""
        )
        pages = []
        if response.full_text_annotation and response.full_text_annotation.pages:
            for page in response.full_text_annotation.pages:
                blocks = []
                for block in page.blocks:
                    paragraphs = []
                    for paragraph in block.paragraphs:
                        words = []
                        for word in paragraph.words:
                            symbols = []
                            for symbol in word.symbols:
                                symbols.append(
                                    {
                                        "text": symbol.text,
                                        "confidence": symbol.confidence,
                                    }
                                )
                            words.append(
                                {
                                    "text": "".join([s["text"] for s in symbols]),
                                    "confidence": word.confidence,
                                }
                            )
                        paragraphs.append(
                            {
                                "text": " ".join([w["text"] for w in words]),
                                "confidence": paragraph.confidence,
                            }
                        )
                    blocks.append(
                        {
                            "text": "\n".join([p["text"] for p in paragraphs]),
                            "confidence": block.confidence,
                        }
                    )
                pages.append(
                    {
                        "text": "\n\n".join([b["text"] for b in blocks]),
                        "confidence": page.confidence,
                    }
                )

        return cls(full_text, pages)


class SafeSearchDetectionResponse:
    def __init__(self, adult: str, spoof: str, medical: str, violence: str, racy: str):
        self.adult = adult
        self.spoof = spoof
        self.medical = medical
        self.violence = violence
        self.racy = racy

    @classmethod
    def from_vision_response(cls, response):
        safe_search = response.safe_search_annotation
        return cls(
            adult=safe_search.adult.name
            if safe_search and safe_search.adult
            else "UNKNOWN",
            spoof=safe_search.spoof.name
            if safe_search and safe_search.spoof
            else "UNKNOWN",
            medical=safe_search.medical.name
            if safe_search and safe_search.medical
            else "UNKNOWN",
            violence=safe_search.violence.name
            if safe_search and safe_search.violence
            else "UNKNOWN",
            racy=safe_search.racy.name
            if safe_search and safe_search.racy
            else "UNKNOWN",
        )


class ImageDescriptionResponse:
    def __init__(self, description: str):
        self.description = description

    @classmethod
    def from_label_detection(cls, label_detection_response: LabelDetectionResponse):
        if not label_detection_response.labels:
            return cls("No clear description based on detected labels.")

        # Simple heuristic: take the top 3 labels with highest score and form a sentence.
        sorted_labels = sorted(
            label_detection_response.labels, key=lambda x: x["score"], reverse=True
        )
        top_labels = [label["description"] for label in sorted_labels[:3]]

        if not top_labels:
            return cls("No clear description based on detected labels.")
        elif len(top_labels) == 1:
            return cls(f"An image featuring {top_labels[0]}.")
        elif len(top_labels) == 2:
            return cls(f"An image featuring {top_labels[0]} and {top_labels[1]}.")
        else:
            return cls(
                f"An image featuring {', '.join(top_labels[:-1])}, and {top_labels[-1]}."
            )
