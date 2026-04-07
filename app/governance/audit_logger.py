from pathlib import Path
from datetime import datetime
import uuid
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUDIT_FILE = PROJECT_ROOT / "data" / "audit_log.csv"


def log_audit_record(result: dict):
    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)

    audit_row = {
        "run_id": str(uuid.uuid4()),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "invoice_id": result.get("invoice_id"),
        "vendor_name": result.get("vendor_name"),
        "issues_found": str(result.get("issues_found")),
        "risk_flag": result.get("risk_flag"),
        "recommendation": result.get("recommendation"),
        "human_decision": result.get("human_decision"),
        "user_role": result.get("user_role"),
        "final_status": result.get("final_status"),
        "final_message": result.get("final_message"),
        "policy_text": result.get("policy_text"),
        "explanation_summary": result.get("explanation_summary"),
        "action_result": result.get("action_result"),
    }

    df_new = pd.DataFrame([audit_row])

    if AUDIT_FILE.exists():
        df_existing = pd.read_csv(AUDIT_FILE)
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_final = df_new

    df_final.to_csv(AUDIT_FILE, index=False)