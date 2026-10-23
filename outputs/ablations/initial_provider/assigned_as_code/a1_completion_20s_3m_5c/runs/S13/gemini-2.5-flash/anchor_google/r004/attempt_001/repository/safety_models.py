class TextModerationRequest:
    def __init__(self, text, languages=None, attributes=None):
        self.text = text
        self.languages = languages or ["en"]
        self.attributes = attributes or {"TOXICITY": {}}

    def to_json(self):
        return {
            "comment": {"text": self.text},
            "languages": self.languages,
            "requestedAttributes": self.attributes,
            "doNotStore": True
        }

class TextModerationResult:
    def __init__(self, response_json):
        self.attribute_scores = {
            attr: score["summaryScore"]["value"]
            for attr, score in response_json.get("attributeScores", {}).items()
        }

    def get_score(self, attribute):
        return self.attribute_scores.get(attribute)

    def to_dict(self):
        return self.attribute_scores
