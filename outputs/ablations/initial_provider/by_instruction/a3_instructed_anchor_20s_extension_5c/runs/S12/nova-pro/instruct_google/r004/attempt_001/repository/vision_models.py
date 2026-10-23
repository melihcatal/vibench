def create_label_request(image_path):
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
    return vision.LabelDetectionRequest(image=image)

def create_description_request(image_path):
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
    return vision.LabelDetectionRequest(image=image)

def create_text_detection_request(image_path):
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
    return vision.TextDetectionRequest(image=image)

def create_safety_request(image_path):
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
    return vision.SafeSearchDetectionRequest(image=image)