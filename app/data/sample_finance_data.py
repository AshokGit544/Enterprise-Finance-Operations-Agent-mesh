import pandas as pd


def get_finance_data():
    data = [
        {
            "invoice_id": "INV1001",
            "vendor_name": "Alpha Energy Services",
            "vendor_id": "V001",
            "cost_center": "CC100",
            "gl_account": "500100",
            "amount_usd": 12000,
            "payment_status": "PAID",
            "invoice_status": "APPROVED",
            "risk_flag": "LOW",
            "policy_text": "Approved invoices under valid vendor and GL mapping can be paid normally."
        },
        {
            "invoice_id": "INV1002",
            "vendor_name": "BlueGrid Technologies",
            "vendor_id": "V002",
            "cost_center": "CC110",
            "gl_account": "500200",
            "amount_usd": 45000,
            "payment_status": "PENDING",
            "invoice_status": "UNDER_REVIEW",
            "risk_flag": "MEDIUM",
            "policy_text": "Invoices above threshold require manager review before payment."
        },
        {
            "invoice_id": "INV1003",
            "vendor_name": "Northwind Electric",
            "vendor_id": None,
            "cost_center": "CC120",
            "gl_account": "500300",
            "amount_usd": 18000,
            "payment_status": "ON_HOLD",
            "invoice_status": "EXCEPTION",
            "risk_flag": "HIGH",
            "policy_text": "Missing vendor master mapping must be investigated before approval."
        },
        {
            "invoice_id": "INV1004",
            "vendor_name": "GreenVolt Contractors",
            "vendor_id": "V004",
            "cost_center": "CC130",
            "gl_account": "500400",
            "amount_usd": -500,
            "payment_status": "ON_HOLD",
            "invoice_status": "EXCEPTION",
            "risk_flag": "HIGH",
            "policy_text": "Negative invoice values are not allowed and must be escalated."
        },
    ]

    return pd.DataFrame(data)