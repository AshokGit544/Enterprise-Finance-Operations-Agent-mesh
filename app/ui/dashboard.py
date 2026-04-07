import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import pandas as pd
import streamlit as st
from app.workflows.finance_graph import build_finance_graph
from app.governance.audit_logger import log_audit_record, AUDIT_FILE
from app.ui.ui_helpers import get_decision_options, get_role_options
from app.utils.report_builder import build_investigation_report


def clear_audit_filters():
    st.session_state["invoice_filter"] = "All"
    st.session_state["status_filter"] = "All"
    st.session_state["invoice_search"] = ""


st.set_page_config(page_title="Enterprise Finance Operations Agent Mesh", layout="wide")

app = build_finance_graph()

st.title("Enterprise Finance Operations Agent Mesh")
st.subheader("Governed LangGraph + Hugging Face Finance Workflow")

# Sidebar
st.sidebar.title("Settings")
developer_mode = st.sidebar.checkbox("Enable Developer Test Mode")

# Workflow Input Section
st.write("## Workflow Input")

invoice_id = st.selectbox(
    "Select Invoice ID",
    ["INV1001", "INV1002", "INV1003", "INV1004", "INV9999"]
)

if developer_mode:
    role_options = ["analyst", "manager", "investigator", "finance_ops", "admin"]
    decision_options = [
        "No human decision required",
        "No human decision applicable",
        "Select manager decision",
        "Select investigation outcome",
        "Select escalation acknowledgement",
        "approved",
        "rejected",
        "resolved",
        "acknowledged",
    ]
else:
    role_options = get_role_options(invoice_id)
    decision_options = get_decision_options(invoice_id)

user_role = st.selectbox(
    "Select User Role",
    role_options
)

human_decision_label = st.selectbox(
    "Optional Human Decision",
    decision_options
)

label_to_value = {
    "No human decision required": "",
    "No human decision applicable": "",
    "Select manager decision": "",
    "Select investigation outcome": "",
    "Select escalation acknowledgement": "",
    "approved": "approved",
    "rejected": "rejected",
    "resolved": "resolved",
    "acknowledged": "acknowledged",
}

human_decision = label_to_value.get(human_decision_label, "")

if st.button("Run Finance Agent"):
    state = {
        "invoice_id": invoice_id,
        "user_role": user_role
    }

    if human_decision:
        state["human_decision"] = human_decision

    result = app.invoke(state)
    log_audit_record(result)

    if result.get("final_status") in ["INVALID_HUMAN_DECISION", "ACCESS_DENIED"]:
        st.error("Workflow completed with governance control failure")
        st.error(result.get("final_message"))
    else:
        st.success("Workflow executed successfully")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Investigation Result")
        st.write(f"**Invoice ID:** {result.get('invoice_id')}")
        st.write(f"**Vendor Name:** {result.get('vendor_name')}")
        st.write(f"**Issues Found:** {result.get('issues_found')}")
        st.write(f"**Risk Flag:** {result.get('risk_flag')}")
        st.write(f"**Recommendation:** {result.get('recommendation')}")
        st.write(f"**Policy Text:** {result.get('policy_text')}")

    with col2:
        st.write("### Final Outcome")
        st.write(f"**User Role:** {result.get('user_role')}")
        st.write(f"**Human Decision:** {result.get('human_decision')}")
        st.write(f"**Final Status:** {result.get('final_status')}")
        st.write(f"**Final Message:** {result.get('final_message')}")
        st.write(f"**Action Result:** {result.get('action_result')}")

    st.write("### Explanation Summary")
    st.write(result.get("explanation_summary"))

    report_text = build_investigation_report(result)
    st.download_button(
        label="Download Investigation Report",
        data=report_text,
        file_name=f"{result.get('invoice_id')}_investigation_report.txt",
        mime="text/plain"
    )

st.write("---")
st.write("## Audit History and Metrics")

# Audit Section
if AUDIT_FILE.exists():
    audit_df = pd.read_csv(AUDIT_FILE)
    audit_df = audit_df.sort_values(by="timestamp", ascending=False)

    total_runs = len(audit_df)
    approved_count = (audit_df["final_status"] == "APPROVED_FOR_PAYMENT").sum()
    manager_approved_count = (audit_df["final_status"] == "MANAGER_APPROVED").sum()
    escalated_count = audit_df["final_status"].isin(
        ["ESCALATED_TO_FINANCE_OPS", "ESCALATION_ACKNOWLEDGED"]
    ).sum()
    invalid_decision_count = (audit_df["final_status"] == "INVALID_HUMAN_DECISION").sum()
    access_denied_count = (audit_df["final_status"] == "ACCESS_DENIED").sum()
    retry_count = (audit_df["final_status"] == "RETRY_REQUIRED").sum()

    m1, m2, m3, m4, m5, m6, m7 = st.columns(7)
    m1.metric("Total Runs", total_runs)
    m2.metric("Approved", approved_count)
    m3.metric("Manager Approved", manager_approved_count)
    m4.metric("Escalated", escalated_count)
    m5.metric("Invalid Decisions", invalid_decision_count)
    m6.metric("Access Denied", access_denied_count)
    m7.metric("Retry Required", retry_count)

    st.write("### Final Status Distribution")
    status_counts = audit_df["final_status"].value_counts()
    st.bar_chart(status_counts)

    st.write("### Workflow Run Trend")
    trend_df = audit_df.copy()
    trend_df["timestamp"] = pd.to_datetime(trend_df["timestamp"], errors="coerce")
    trend_df["run_date"] = trend_df["timestamp"].dt.date

    daily_runs = (
        trend_df.groupby("run_date")
        .size()
        .reset_index(name="run_count")
        .sort_values("run_date")
    )

    if not daily_runs.empty:
        daily_runs["run_date"] = pd.to_datetime(daily_runs["run_date"])
        st.line_chart(daily_runs.set_index("run_date")["run_count"])
    else:
        st.info("No trend data available yet.")

    st.write("### Role-Based Action Summary")
    if "user_role" in audit_df.columns:
        role_counts = audit_df["user_role"].fillna("unknown").value_counts()
        st.bar_chart(role_counts)
    else:
        st.info("No role data available yet.")

    st.write("### Governance Failure Summary")
    failure_df = audit_df[
        audit_df["final_status"].isin(["INVALID_HUMAN_DECISION", "ACCESS_DENIED"])
    ]

    if not failure_df.empty:
        failure_counts = failure_df["final_status"].value_counts()
        st.bar_chart(failure_counts)
    else:
        st.info("No governance failures recorded yet.")

    st.write("### Audit Filters")

    if "invoice_filter" not in st.session_state:
        st.session_state["invoice_filter"] = "All"
    if "status_filter" not in st.session_state:
        st.session_state["status_filter"] = "All"
    if "invoice_search" not in st.session_state:
        st.session_state["invoice_search"] = ""

    f1, f2, f3, f4 = st.columns([1, 1, 1, 0.8])

    with f1:
        st.selectbox(
            "Filter by Invoice ID",
            ["All"] + sorted(audit_df["invoice_id"].dropna().astype(str).unique().tolist()),
            key="invoice_filter"
        )

    with f2:
        st.selectbox(
            "Filter by Final Status",
            ["All"] + sorted(audit_df["final_status"].dropna().astype(str).unique().tolist()),
            key="status_filter"
        )

    with f3:
        st.text_input("Search Invoice ID", key="invoice_search")

    with f4:
        st.write("")
        st.write("")
        st.button("Clear Filters", on_click=clear_audit_filters)

    filtered_df = audit_df.copy()

    if st.session_state["invoice_filter"] != "All":
        filtered_df = filtered_df[
            filtered_df["invoice_id"].astype(str) == st.session_state["invoice_filter"]
        ]

    if st.session_state["status_filter"] != "All":
        filtered_df = filtered_df[
            filtered_df["final_status"].astype(str) == st.session_state["status_filter"]
        ]

    if st.session_state["invoice_search"].strip():
        filtered_df = filtered_df[
            filtered_df["invoice_id"].astype(str).str.contains(
                st.session_state["invoice_search"].strip(),
                case=False,
                na=False
            )
        ]

    preferred_columns = [
        "run_id",
        "timestamp",
        "invoice_id",
        "vendor_name",
        "user_role",
        "human_decision",
        "final_status",
        "final_message",
        "action_result",
        "recommendation",
        "risk_flag",
    ]

    visible_columns = [col for col in preferred_columns if col in filtered_df.columns]

    st.write("### Audit Table")
    st.dataframe(filtered_df[visible_columns], use_container_width=True)

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Filtered Audit Log CSV",
        data=csv_data,
        file_name="filtered_audit_log.csv",
        mime="text/csv"
    )

    st.write("### Run Detail Viewer")

    if "run_id" in audit_df.columns:
        run_options = audit_df["run_id"].dropna().astype(str).unique().tolist()
        selected_run_id = st.selectbox("Select Run ID", run_options)

        selected_run = audit_df[audit_df["run_id"].astype(str) == selected_run_id]

        if not selected_run.empty:
            row = selected_run.iloc[0]

            c1, c2 = st.columns(2)

            with c1:
                st.write("#### Run Core Details")
                st.write(f"**Run ID:** {row.get('run_id')}")
                st.write(f"**Timestamp:** {row.get('timestamp')}")
                st.write(f"**Invoice ID:** {row.get('invoice_id')}")
                st.write(f"**Vendor Name:** {row.get('vendor_name')}")
                st.write(f"**User Role:** {row.get('user_role')}")
                st.write(f"**Human Decision:** {row.get('human_decision')}")

            with c2:
                st.write("#### Run Outcome Details")
                st.write(f"**Final Status:** {row.get('final_status')}")
                st.write(f"**Final Message:** {row.get('final_message')}")
                st.write(f"**Action Result:** {row.get('action_result')}")
                st.write(f"**Recommendation:** {row.get('recommendation')}")
                st.write(f"**Risk Flag:** {row.get('risk_flag')}")

            if "policy_text" in row.index:
                st.write("#### Policy Text")
                st.info(str(row.get("policy_text")))

            if "explanation_summary" in row.index:
                st.write("#### Explanation Summary")
                st.write(str(row.get("explanation_summary")))
    else:
        st.info("Run detail viewer is not available because run_id is missing in the audit file.")
else:
    st.info("No audit history found yet. Run the workflow first.")