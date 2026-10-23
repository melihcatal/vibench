class VisionRequest:
    def __init__(self, image_path):
        with open(image_path, 'rb') as image_file:
            self.content = image_file.read()

class VisionResponse:
    def __init__(self, response):
        self.response = response

    def get_labels(self):
        return [{'description': label['description'],'score': label['score']} for label in self.response['labelAnnotations']]

    def get_text(self):
        if 'fullTextAnnotation' in self.response:
            return self.response['fullTextAnnotation']['text']
        return ''

    def get_safety(self):
        safety = self.response['safeSearchAnnotation']
        return {'adult': safety['adult'],'medical': safety['medical'],'spoof': safety['spoof'], 'violence': safety['violence'], 'racy': safety['racy']}
