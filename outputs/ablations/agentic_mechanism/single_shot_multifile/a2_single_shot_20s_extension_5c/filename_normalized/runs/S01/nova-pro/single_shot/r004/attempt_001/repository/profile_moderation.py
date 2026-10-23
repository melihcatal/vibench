import os
from perspective_api import PerspectiveAPI

def moderate_profile_text(text):
    api = PerspectiveAPI()
    result = api.analyze(text)
    return result
