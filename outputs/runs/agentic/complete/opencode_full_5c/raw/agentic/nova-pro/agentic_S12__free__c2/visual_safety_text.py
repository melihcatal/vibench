import boto3


def check_safety(labels):
    unsafe_words = ["violence", "nudity"]
    for label in labels:
        if any(word in label.lower() for word in unsafe_words):
            return False
    return True
