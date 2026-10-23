from vision_client import get_vision_client, get_image
from vision_models import normalize_labels, normalize_text, normalize_safety

def summarize_analysis(image_path):
    client = get_vision_client()
    image = get_image(image_path)
    label_response = client.label_detection(image=image)
    text_response = client.text_detection(image=image)
    safety_response = client.safe_search_detection(image=image)
    labels = normalize_labels(label_response)
    texts = normalize_text(text_response)
    safety = normalize_safety(safety_response)
    print('Summary:')
    print('Labels:', labels)
    print('Texts:', texts)
    print('Safety:', safety)

if __name__ == '__main__':
    summarize_analysis('path/to/image.jpg')