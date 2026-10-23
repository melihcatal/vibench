from moderate_text import moderate_text
import os


def safety_threshold(text, thresholds=None):
    if thresholds is None:
        thresholds = {
            "TOXICITY": 0.7,
            "SEVERE_TOXICITY": 0.5,
            "IDENTITY_ATTACK": 0.6,
            "INSULT": 0.7,
            "PROFANITY": 0.8,
            "THREAT": 0.9,
        }

    scores = moderate_text(text, attributes=list(thresholds.keys()))

    for category, threshold_value in thresholds.items():
        if scores.get(category, 0.0) > threshold_value:
            return (
                False,
                f"Text blocked due to {category} score ({scores.get(category):.2f}) exceeding threshold ({threshold_value}).",
            )
    return True, "Text allowed."


if __name__ == "__main__":
    # Example usage (requires PERSPECTIVE_API_KEY environment variable to be set)
    # os.environ["PERSPECTIVE_API_KEY"] = "YOUR_PERSPECTIVE_API_KEY"
    if "PERSPECTIVE_API_KEY" not in os.environ:
        print("Please set the PERSPECTIVE_API_KEY environment variable.")
    else:
        text_to_check = "You are a terrible person."
        allowed, reason = safety_threshold(text_to_check)
        print(f"Text: '{text_to_check}', Allowed: {allowed}, Reason: {reason}")

        text_to_check_2 = "This is a perfectly fine message."
        allowed_2, reason_2 = safety_threshold(text_to_check_2)
        print(f"Text: '{text_to_check_2}', Allowed: {allowed_2}, Reason: {reason_2}")

        custom_thresholds = {"TOXICITY": 0.2}
        text_to_check_3 = "This is a bit rude."
        allowed_3, reason_3 = safety_threshold(
            text_to_check_3, thresholds=custom_thresholds
        )
        print(f"Text: '{text_to_check_3}', Allowed: {allowed_3}, Reason: {reason_3}")
