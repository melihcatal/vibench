import os

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
EVENTS_TOPIC = os.getenv("EVENTS_TOPIC", "events")
EVENTS_SUB = os.getenv("EVENTS_SUB", "events-sub")
DEAD_LETTER_TOPIC = os.getenv("DEAD_LETTER_TOPIC", "dead-letters")
