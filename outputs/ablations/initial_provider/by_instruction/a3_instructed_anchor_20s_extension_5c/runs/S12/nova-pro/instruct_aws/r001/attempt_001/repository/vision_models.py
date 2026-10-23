class VisionModels:
    @staticmethod
    def normalize_labels(response):
        return [label['Name'] for label in response['Labels']]

    @staticmethod
    def normalize_text(response):
        return [detection['DetectedText'] for detection in response['TextDetections']]

    @staticmethod
    def normalize_safety(response):
        return [label['Name'] for label in response['ModerationLabels']]