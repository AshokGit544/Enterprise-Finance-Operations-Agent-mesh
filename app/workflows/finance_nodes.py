from app.data.sample_finance_data import get_finance_data
from app.tools.finance_investigator import investigate_invoice
from app.embeddings.policy_search import search_relevant_policy
from app.agents.finance_explainer import generate_explanation
from app.governance.decision_validator import validate_human_decision
from app.governance.rbac import is_action_allowed
from app.tools.action_executor import (
    create_payment_release,
    create_manager_approval_record,
    create_investigation_closure,
    create_escalation_case,
    create_governance_alert,
)


def investigation_node(state):
    df = get_finance_data()

    record = df[df["invoice_id"] == state["invoice_id"]]

    if record.empty:
        policy = {
            "text": "If an invoice record is not found, the invoice identifier must be verified and the request should be retried."
        }
        return {
            "invoice_id": state["invoice_id"],
            "vendor_name": None,
            "issues_found": ["Invoice not found"],
            "risk_flag": "UNKNOWN",
            "policy_text": policy["text"],
            "recommendation": "Check invoice ID and retry",
            "human_decision": state.get("human_decision", ""),
            "user_role": state.get("user_role", "")
        }

    result = investigate_invoice(record.iloc[0].to_dict())
    result["human_decision"] = state.get("human_decision", "")
    result["user_role"] = state.get("user_role", "")

    issue_text = " ".join(result["issues_found"]).lower()
    recommendation_text = result["recommendation"].lower()
    risk_text = str(result.get("risk_flag", "")).lower()
    vendor_text = result.get("vendor_name", "") or ""

    if "invalid invoice amount" in issue_text or "escalate" in recommendation_text:
        policy = {
            "text": "Invoices with negative values are invalid and must be escalated to finance operations immediately."
        }
    elif "missing vendor_id" in issue_text:
        policy = {
            "text": "Invoices with missing vendor master mapping must be held and investigated before any approval or payment action."
        }
    elif "invoice not found" in issue_text:
        policy = {
            "text": "If an invoice record is not found, the invoice identifier must be verified and the request should be retried."
        }
    else:
        semantic_query = f"""
        invoice investigation
        vendor {vendor_text}
        issues {issue_text}
        recommendation {recommendation_text}
        risk {risk_text}
        """
        policy = search_relevant_policy(semantic_query)

    result["policy_text"] = policy["text"]
    return result


def route_decision(state):
    recommendation = state.get("recommendation", "").lower()

    if "approve" in recommendation:
        return "approve_path"
    elif "manager approval" in recommendation:
        return "review_path"
    elif "escalate" in recommendation:
        return "escalate_path"
    elif "investigate" in recommendation or "hold" in recommendation:
        return "manual_investigation_path"
    else:
        return "retry_path"


def approve_node(state):
    decision = str(state.get("human_decision", "")).lower()
    role = str(state.get("user_role", "")).lower()

    is_valid, message = validate_human_decision(state.get("recommendation", ""), decision)
    is_allowed, access_message = is_action_allowed(role, state.get("recommendation", ""), decision)

    if not is_valid and decision:
        state["final_status"] = "INVALID_HUMAN_DECISION"
        state["final_message"] = message
        state["action_result"] = create_governance_alert(state["invoice_id"], message)
    elif not is_allowed and decision:
        state["final_status"] = "ACCESS_DENIED"
        state["final_message"] = access_message
        state["action_result"] = create_governance_alert(state["invoice_id"], access_message)
    else:
        state["final_status"] = "APPROVED_FOR_PAYMENT"
        state["final_message"] = "Invoice passed checks and is approved for payment."
        state["action_result"] = create_payment_release(state["invoice_id"])

    state["explanation_summary"] = generate_explanation(state)
    return state


def review_node(state):
    decision = str(state.get("human_decision", "")).lower()
    role = str(state.get("user_role", "")).lower()

    is_valid, message = validate_human_decision(state.get("recommendation", ""), decision)
    is_allowed, access_message = is_action_allowed(role, state.get("recommendation", ""), decision)

    if not is_valid and decision:
        state["final_status"] = "INVALID_HUMAN_DECISION"
        state["final_message"] = message
        state["action_result"] = create_governance_alert(state["invoice_id"], message)
    elif not is_allowed and decision:
        state["final_status"] = "ACCESS_DENIED"
        state["final_message"] = access_message
        state["action_result"] = create_governance_alert(state["invoice_id"], access_message)
    elif decision == "approved":
        state["final_status"] = "MANAGER_APPROVED"
        state["final_message"] = "Manager reviewed the invoice and approved it for payment."
        state["action_result"] = create_manager_approval_record(state["invoice_id"])
    elif decision == "rejected":
        state["final_status"] = "MANAGER_REJECTED"
        state["final_message"] = "Manager reviewed the invoice and rejected it."
        state["action_result"] = create_governance_alert(state["invoice_id"], "Manager rejected invoice")
    else:
        state["final_status"] = "PENDING_MANAGER_REVIEW"
        state["final_message"] = "Invoice requires manager approval before payment."
        state["action_result"] = "No downstream action executed yet"

    state["explanation_summary"] = generate_explanation(state)
    return state


def escalate_node(state):
    decision = str(state.get("human_decision", "")).lower()
    role = str(state.get("user_role", "")).lower()

    is_valid, message = validate_human_decision(state.get("recommendation", ""), decision)
    is_allowed, access_message = is_action_allowed(role, state.get("recommendation", ""), decision)

    if not is_valid and decision:
        state["final_status"] = "INVALID_HUMAN_DECISION"
        state["final_message"] = message
        state["action_result"] = create_governance_alert(state["invoice_id"], message)
    elif not is_allowed and decision:
        state["final_status"] = "ACCESS_DENIED"
        state["final_message"] = access_message
        state["action_result"] = create_governance_alert(state["invoice_id"], access_message)
    elif decision == "acknowledged":
        state["final_status"] = "ESCALATION_ACKNOWLEDGED"
        state["final_message"] = "Finance operations acknowledged the escalation and will take corrective action."
        state["action_result"] = create_escalation_case(state["invoice_id"])
    else:
        state["final_status"] = "ESCALATED_TO_FINANCE_OPS"
        state["final_message"] = "Invoice has critical issues and was escalated to finance operations."
        state["action_result"] = "Escalation pending acknowledgement"

    state["explanation_summary"] = generate_explanation(state)
    return state


def manual_investigation_node(state):
    decision = str(state.get("human_decision", "")).lower()
    role = str(state.get("user_role", "")).lower()

    is_valid, message = validate_human_decision(state.get("recommendation", ""), decision)
    is_allowed, access_message = is_action_allowed(role, state.get("recommendation", ""), decision)

    if not is_valid and decision:
        state["final_status"] = "INVALID_HUMAN_DECISION"
        state["final_message"] = message
        state["action_result"] = create_governance_alert(state["invoice_id"], message)
    elif not is_allowed and decision:
        state["final_status"] = "ACCESS_DENIED"
        state["final_message"] = access_message
        state["action_result"] = create_governance_alert(state["invoice_id"], access_message)
    elif decision == "resolved":
        state["final_status"] = "INVESTIGATION_RESOLVED"
        state["final_message"] = "Manual investigation completed and the issue was resolved."
        state["action_result"] = create_investigation_closure(state["invoice_id"])
    else:
        state["final_status"] = "PENDING_MANUAL_INVESTIGATION"
        state["final_message"] = "Invoice is on hold and requires manual investigation before any action."
        state["action_result"] = "Investigation still pending"

    state["explanation_summary"] = generate_explanation(state)
    return state


def retry_node(state):
    decision = str(state.get("human_decision", "")).lower()
    role = str(state.get("user_role", "")).lower()

    is_valid, message = validate_human_decision(state.get("recommendation", ""), decision)
    is_allowed, access_message = is_action_allowed(role, state.get("recommendation", ""), decision)

    if not is_valid and decision:
        state["final_status"] = "INVALID_HUMAN_DECISION"
        state["final_message"] = message
        state["action_result"] = create_governance_alert(state["invoice_id"], message)
    elif not is_allowed and decision:
        state["final_status"] = "ACCESS_DENIED"
        state["final_message"] = access_message
        state["action_result"] = create_governance_alert(state["invoice_id"], access_message)
    else:
        state["final_status"] = "RETRY_REQUIRED"
        state["final_message"] = "Invoice could not be processed. Please verify invoice ID and retry."
        state["action_result"] = "Retry requested - no downstream action executed"

    state["explanation_summary"] = generate_explanation(state)
    return state