def is_action_allowed(user_role: str, recommendation: str, human_decision: str):
    user_role = (user_role or "").lower()
    recommendation = (recommendation or "").lower()
    human_decision = (human_decision or "").lower()

    permissions = {
        "analyst": [],
        "manager": ["approved", "rejected"],
        "investigator": ["resolved"],
        "finance_ops": ["acknowledged"],
        "admin": ["approved", "rejected", "resolved", "acknowledged"],
    }

    allowed_actions = permissions.get(user_role, [])

    if not human_decision:
        return True, "No human action requested"

    if human_decision in allowed_actions:
        return True, f"Role '{user_role}' is allowed to perform '{human_decision}'"

    return False, f"Access denied: role '{user_role}' cannot perform '{human_decision}'"