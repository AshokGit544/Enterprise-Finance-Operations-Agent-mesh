def build_investigation_report(result: dict) -> str:
    report = f"""
Enterprise Finance Operations Agent Mesh - Investigation Report

Invoice ID: {result.get('invoice_id')}
Vendor Name: {result.get('vendor_name')}
User Role: {result.get('user_role')}
Human Decision: {result.get('human_decision')}

Issues Found: {result.get('issues_found')}
Risk Flag: {result.get('risk_flag')}
Recommendation: {result.get('recommendation')}

Final Status: {result.get('final_status')}
Final Message: {result.get('final_message')}
Action Result: {result.get('action_result')}

Policy Text:
{result.get('policy_text')}

Explanation Summary:
{result.get('explanation_summary')}
""".strip()

    return report