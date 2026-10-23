from perspectiveapi import PerspectiveAPI

def moderate_text(text):
    api = PerspectiveAPI(os.getenv('PERSPECTIVE_API_KEY'))
    result = api.analyze(text)
    return result