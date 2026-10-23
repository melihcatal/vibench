from typing import List, Dict, Any

class ModerationRequest:
    def __init__(self, text: str, context: Dict = None):
        self.text = text
        self.context = context if context is not None else {}

    def to_dict(self):
        return {"text": self.text, "context": self.context}

class ModerationResponse:
    def __init__(self, 
                 overall_decision: str, 
                 category_scores: Dict[str, float], 
                 flags: List[str] = None,
                 raw_response: Any = None):
        self.overall_decision = overall_decision
        self.category_scores = category_scores
        self.flags = flags if flags is not None else []
        self.raw_response = raw_response

    def to_dict(self):
        return {
            "overall_decision": self.overall_decision,
            "category_scores": self.category_scores,
            "flags": self.flags,
            "raw_response": str(self.raw_response) # Convert raw_response to string for serialization
        }

def normalize_gemini_response(gemini_response: Any) -> ModerationResponse:
    # This is a simplified normalization. Actual implementation would parse Gemini's specific safety_ratings structure.
    overall_decision = "UNKNOWN"
    category_scores = {}
    flags = []

    if gemini_response and gemini_response.candidates:
        safety_ratings = gemini_response.candidates[0].safety_ratings
        for rating in safety_ratings:
            category = rating.category.split('_', 2)[-1] # Extract category name, e.g., HARASSMENT
            category_scores[category] = rating.score # Assuming score is numeric or can be mapped
            if rating.probability != "BLOCK_NONE": # A heuristic for flagging
                flags.append(category)
        
        # Determine overall decision based on any flags
        if flags:
            overall_decision = "BLOCKED"
        else:
            overall_decision = "ALLOWED"


    return ModerationResponse(
        overall_decision=overall_decision,
        category_scores=category_scores,
        flags=flags,
        raw_response=gemini_response
    )
