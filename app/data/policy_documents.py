def get_policy_documents():
    return [
        {
            "policy_id": "POL001",
            "title": "Valid Vendor Policy",
            "category": "approval",
            "keywords": "valid vendor master mapping approved payment normal invoice",
            "text": "Invoices with valid vendor master mapping, valid GL mapping, and no exception indicators can be approved for normal payment processing."
        },
        {
            "policy_id": "POL002",
            "title": "Invoice Threshold Review Policy",
            "category": "manager_review",
            "keywords": "threshold amount manager review approval pending high amount",
            "text": "Invoices above the approval threshold must be reviewed and approved by a manager before payment."
        },
        {
            "policy_id": "POL003",
            "title": "Negative Amount Escalation Policy",
            "category": "escalation",
            "keywords": "negative invalid amount escalate finance operations",
            "text": "Invoices with negative values are invalid and must be escalated to finance operations immediately."
        },
        {
            "policy_id": "POL004",
            "title": "Invoice Exception Handling Policy",
            "category": "manual_investigation",
            "keywords": "exception hold investigate manual review issue resolution",
            "text": "Invoices in exception state must be placed on hold until the issue is manually investigated and resolved."
        },
        {
            "policy_id": "POL005",
            "title": "Missing Vendor Mapping Policy",
            "category": "manual_investigation",
            "keywords": "missing vendor master mapping hold investigate vendor validation",
            "text": "Invoices with missing vendor master mapping must be held and investigated before any approval or payment action."
        },
        {
            "policy_id": "POL006",
            "title": "Invoice Retry Validation Policy",
            "category": "retry",
            "keywords": "invoice not found retry validation verify invoice identifier",
            "text": "If an invoice record is not found, the invoice identifier must be verified and the request should be retried."
        },
    ]