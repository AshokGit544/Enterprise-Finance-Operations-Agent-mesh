def investigate_invoice(record: dict) -> dict:
    issues = []
    recommendation = "Approve for payment"

    if not record.get("vendor_id"):
        issues.append("Missing vendor_id")
        recommendation = "Hold and investigate vendor mapping"

    if record.get("amount_usd", 0) <= 0:
        issues.append("Invalid invoice amount")
        recommendation = "Escalate to finance operations"

    if record.get("invoice_status") == "UNDER_REVIEW":
        issues.append("Invoice requires manager review")
        recommendation = "Send for manager approval"

    if record.get("invoice_status") == "EXCEPTION":
        issues.append("Invoice is in exception state")
        if recommendation == "Approve for payment":
            recommendation = "Hold for manual investigation"

    if not issues:
        issues.append("No major issue detected")

    return {
        "invoice_id": record.get("invoice_id"),
        "vendor_name": record.get("vendor_name"),
        "issues_found": issues,
        "risk_flag": record.get("risk_flag"),
        "policy_text": record.get("policy_text"),
        "recommendation": recommendation
    }