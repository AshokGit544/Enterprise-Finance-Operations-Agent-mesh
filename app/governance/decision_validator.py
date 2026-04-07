def validate_human_decision(recommendation: str, human_decision: str):
    recommendation = (recommendation or "").lower()
    human_decision = (human_decision or "").lower()

    if "manager approval" in recommendation:
        allowed = ["approved", "rejected"]
    elif "investigate" in recommendation or "hold" in recommendation:
        allowed = ["resolved"]
    elif "escalate" in recommendation:
        allowed = ["acknowledged"]
    elif "approve" in recommendation:
        allowed = [""]
    else:
        allowed = [""]

    if human_decision in allowed:
        return True, "Valid human decision"

    return False, f"Invalid human decision '{human_decision}' for recommendation '{recommendation}'"