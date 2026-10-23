import vision_models

def image_summary(objects, caption, text, adult):
    response = vision_models.VisionResponse(objects, caption, text, adult)
    return f'Objects: {response.objects}, Caption: {response.caption}, Text: {response.text}, Adult: {response.adult}'