from enum import Enum

class ContentCategory(str, Enum):
    VIOLENCE = "Violence"
    HATE_SPEECH = "Hate"
    SEXUAL = "Sexual"
    SELF_HARM = "SelfHarm"

class SeverityLevel(int, Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
