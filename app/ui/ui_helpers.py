from app.data.sample_finance_data import get_finance_data
from app.tools.finance_investigator import investigate_invoice


def get_decision_options(invoice_id: str):
    df = get_finance_data()
    record = df[df["invoice_id"] == invoice_id]

    if record.empty:
        return ["No human decision applicable"]

    result = investigate_invoice(record.iloc[0].to_dict())
    recommendation = result.get("recommendation", "").lower()

    if "manager approval" in recommendation:
        return ["Select manager decision", "approved", "rejected"]
    elif "investigate" in recommendation or "hold" in recommendation:
        return ["Select investigation outcome", "resolved"]
    elif "escalate" in recommendation:
        return ["Select escalation acknowledgement", "acknowledged"]
    elif "approve" in recommendation:
        return ["No human decision required"]
    else:
        return ["No human decision applicable"]


def get_role_options(invoice_id: str):
    df = get_finance_data()
    record = df[df["invoice_id"] == invoice_id]

    if record.empty:
        return ["analyst", "admin"]

    result = investigate_invoice(record.iloc[0].to_dict())
    recommendation = result.get("recommendation", "").lower()

    if "manager approval" in recommendation:
        return ["manager", "admin"]
    elif "investigate" in recommendation or "hold" in recommendation:
        return ["investigator", "admin"]
    elif "escalate" in recommendation:
        return ["finance_ops", "admin"]
    elif "approve" in recommendation:
        return ["analyst", "manager", "admin"]
    else:
        return ["analyst", "admin"]