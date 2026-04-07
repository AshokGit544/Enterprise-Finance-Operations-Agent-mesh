def generate_explanation(state: dict) -> str:
    invoice_id = state.get("invoice_id", "UNKNOWN")
    vendor_name = state.get("vendor_name", "Unknown Vendor")
    issues = ", ".join(state.get("issues_found", []))
    risk_flag = state.get("risk_flag", "UNKNOWN")
    recommendation = state.get("recommendation", "No recommendation available")
    final_status = state.get("final_status", "UNKNOWN")
    policy_text = state.get("policy_text", "No policy available")
    human_decision = state.get("human_decision", "No human decision provided")

    summary = (
        f"Invoice {invoice_id} for vendor {vendor_name} was evaluated by the finance operations agent. "
        f"The main issues identified were: {issues}. "
        f"The case was classified with risk level {risk_flag}. "
        f"The system recommendation was: {recommendation}. "
        f"The final workflow status is: {final_status}. "
        f"Relevant finance policy states: {policy_text} "
        f"Human decision recorded: {human_decision}."
    )

    return summary