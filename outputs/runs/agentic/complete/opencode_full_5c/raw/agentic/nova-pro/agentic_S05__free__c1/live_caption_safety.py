import os
from google.cloud import contentsafety_v1


def live_caption_safety(text):
    client = contentsafety_v1.ContentSafetyClient()
    parent = "projects/YOUR_PROJECT_ID"
    request = contentsafety_v1.TextSafetyRequest(text=text)
    response = client.text_safety(request=request, parent=parent)
    return response.categories
