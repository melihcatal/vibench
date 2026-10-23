def handle_recognition_event(event):
    if "results" in event:
        for result in event["results"]:
            if result["is_final"]:
                print("Final transcript:", result["alternatives"][0]["transcript"])
            else:
                print("Interim transcript:", result["alternatives"][0]["transcript"])
