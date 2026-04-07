from typing import TypedDict, Optional


class FinanceAgentState(TypedDict, total=False):
    invoice_id: str
    vendor_name: Optional[str]
    issues_found: list
    risk_flag: Optional[str]
    policy_text: Optional[str]
    recommendation: Optional[str]
    final_status: Optional[str]
    final_message: Optional[str]
    human_decision: Optional[str]
    human_comment: Optional[str]
    explanation_summary: Optional[str]
    user_role: Optional[str]
    action_result: Optional[str]