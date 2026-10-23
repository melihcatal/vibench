from vision_models import VisionResponse

def check_safety(vision_response):
    unsafe_words = ['unsafe', 'sensitive']
    labels = vision_response.labels.split(', ')
    unsafe_labels = [label for label in labels if any(word in label for word in unsafe_words)]
    if unsafe_labels:
        print('Unsafe Labels:', unsafe_labels)