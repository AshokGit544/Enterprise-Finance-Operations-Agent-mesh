from app.workflows.finance_graph import build_finance_graph
from app.governance.audit_logger import log_audit_record

app = build_finance_graph()

test_inputs = [
    {"invoice_id": "INV1001"},
    {"invoice_id": "INV1002", "human_decision": "approved"},
    {"invoice_id": "INV1003", "human_decision": "resolved"},
    {"invoice_id": "INV1004", "human_decision": "acknowledged"},
    {"invoice_id": "INV9999"},
]

for state in test_inputs:
    result = app.invoke(state)
    log_audit_record(result)

    print("=" * 100)
    print(f"Invoice ID      : {result['invoice_id']}")
    print(f"Vendor Name     : {result.get('vendor_name')}")
    print(f"Issues Found    : {result.get('issues_found')}")
    print(f"Risk Flag       : {result.get('risk_flag')}")
    print(f"Policy Text     : {result.get('policy_text')}")
    print(f"Recommendation  : {result.get('recommendation')}")
    print(f"Human Decision  : {result.get('human_decision')}")
    print(f"Final Status    : {result.get('final_status')}")
    print(f"Final Message   : {result.get('final_message')}")
    print(f"Explanation     : {result.get('explanation_summary')}")

print("\nAudit log written to data/audit_log.csv")