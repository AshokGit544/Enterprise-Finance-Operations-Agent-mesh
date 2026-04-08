# Enterprise Finance Operations Agent Mesh:

Live Demo
You can explore the live Streamlit application here:
https://enterprise-finance-operations-agent-mesh-rrmxswfahdgtoxjnxrbdw.streamlit.app

Enterprise Finance Operations Agent Mesh:

Enterprise Finance Operations Agent Mesh is a governed finance workflow project that simulates how an enterprise team can investigate invoice issues, follow policy guidance, validate human decisions, and maintain an audit trail in one place.

I built this project to go beyond a normal chatbot or simple dashboard. The idea was to create something closer to a real enterprise workflow tool where the system does not just answer a question, but actually checks the case, routes it to the correct path, validates actions, and records everything for review.

This project uses LangGraph for workflow orchestration, Hugging Face for semantic policy retrieval, Streamlit for the dashboard, and Python for the full backend logic. The workflow supports invoice investigation, human-in-the-loop control, policy grounding, audit logging, explanation generation, dashboard analytics, and filtered audit review.  

Project idea

In enterprise finance operations, invoice cases are not always simple. Some invoices are clean and can move forward. Some need manager review. Some have missing vendor mapping. Some must be escalated because the amount is invalid. Some cannot even be found and need a retry.

In real business environments, these cases should not be handled by a basic if else script or a simple Q and A chatbot. They need workflow logic, policy support, human validation, and traceability.

That is what this project demonstrates.

What this project does

The user selects an invoice in the dashboard and optionally gives a human decision when the workflow requires one.

The system then reads the invoice record, investigates the case, finds the most relevant policy, routes the invoice to the correct workflow path, validates whether the chosen action is allowed, creates a final outcome, generates an explanation summary, and writes the full result into audit history.

Main workflow paths

This project supports five main paths.

Approve for payment

This happens when the invoice is clean and no major issue is found. In this case, no human decision is required.

Manager review

This happens when the invoice requires approval from a manager. In this case, the valid human decisions are approved or rejected.

Manual investigation

This happens when the invoice has a business issue such as missing vendor mapping. In this case, the valid human decision is resolved after investigation is completed.

Escalation

This happens when the invoice has a critical issue such as an invalid negative amount. In this case, the valid human decision is acknowledged by finance operations.

Retry required

This happens when the invoice is not found. In this case, no normal business decision is allowed and the user needs to verify the invoice and retry.

Why this project is different

This project is not just a dashboard and not just a retrieval demo.

It combines workflow orchestration, semantic policy retrieval, rule-based control, human decision validation, governed actions, explanation generation, and audit visibility in one place.

That is what makes it more advanced and more realistic than a normal finance copilot or simple RAG app. The uploaded notes also position it as a stronger 2026-style governed agentic system rather than another standard chatbot project.

Core features

LangGraph based workflow routing

Hugging Face semantic policy search

Hybrid rule based and semantic control logic

Human decision validation

Governed finance workflow execution

Audit logging with run history

Explanation summary for each run

Streamlit dashboard for business users

KPI cards for workflow monitoring

Final status distribution chart

Audit filters and invoice search

Filtered CSV export

Clear filters support in audit review

Dynamic human decision options based on workflow stage

How the dashboard works

The dashboard is the main user interface of this project.

A user can choose an invoice ID from the dropdown and then see only the human decision options that make sense for that workflow path.

For example, a clean invoice should show that no human decision is required. A manager review case should only allow approved or rejected. A manual investigation case should only allow resolved. An escalation case should only allow acknowledged.

After the user runs the workflow, the dashboard shows the investigation result, the final workflow outcome, the supporting policy text, and a business-friendly explanation summary.

Below that, the dashboard also shows audit history, KPI metrics, charts, filters, and CSV export so the user can review earlier runs in a simple way.

Business value

This project shows how enterprise AI can be made more useful and safer for finance operations.

Instead of only answering questions, the system supports structured investigation, controlled routing, valid decision handling, and auditable outcomes.

This kind of design is useful for compliance review, governance checks, exception handling, operational monitoring, and human approval workflows. 

Tech stack

Python

Pandas

Streamlit

LangGraph

LangChain ecosystem

Hugging Face Sentence Transformers

FAISS

Governance and validation logic

Audit logging and workflow analytics 

Folder structure

Enterprise-Finance-Operations-Agent-Mesh

app

agents
finance_explainer.py

config

data
policy_documents.py
sample_finance_data.py

embeddings
policy_search.py

governance
audit_logger.py
decision_validator.py
rbac.py

tools
action_executor.py
finance_investigator.py

ui
dashboard.py
ui_helpers.py

utils
report_builder.py

workflows
finance_graph.py
finance_nodes.py
finance_state.py

data
audit_log.csv

notebooks

tests

main.py

README.md

requirements.txt

.env 

How the code is organized

The workflows folder holds the LangGraph workflow logic and shared state.

The tools folder contains business logic for invoice investigation and controlled action execution.

The governance folder contains audit logging, decision validation, and role based access logic.

The embeddings folder handles semantic policy search using Hugging Face models.

The agents folder contains the explanation generation logic.

The ui folder contains the Streamlit dashboard and helper logic for dynamic controls.

The data folder contains sample finance records and policy documents used by the workflow. 

How to run this project in VS Code

Open the project folder in VS Code.

Open the terminal.

Create a virtual environment by running

python -m venv venv

Activate the virtual environment on Windows by running

.\venv\Scripts\Activate.ps1

Install dependencies by running

pip install -r requirements.txt

Run the dashboard by using

python -m streamlit run app/ui/dashboard.py

After that, the dashboard should open in your browser. 

Example use cases

Manager approval example

Use invoice INV1002 and choose approved.

Expected result is a manager approved outcome, a workflow record, and a new audit entry.

Manual investigation example

Use invoice INV1003 and choose resolved.

Expected result is an investigation resolved outcome and a new audit entry.

Escalation acknowledgement example

Use invoice INV1004 and choose acknowledged.

Expected result is an escalation acknowledged outcome and a new audit entry.

Retry example

Use invoice INV9999.

Expected result is retry required because the invoice record is not found.

Governance failure example

Choose a wrong human decision for a workflow path that does not allow it.

Expected result is an invalid human decision outcome and a matching audit entry.

What I learned from building this

While building this project, I focused on one important idea.

Enterprise AI should not just be smart. It should also be controlled, explainable, and traceable.

That is why this project does not stop at retrieval or recommendation. It also validates human actions, records every run, supports dashboard monitoring, and makes the workflow easier to review through filters, charts, and history.

Why this project matters for modern AI work

A lot of AI demos stop at chat or search. This project shows a more practical direction.

It demonstrates how AI can support finance operations through governed workflows, controlled decisions, policy grounding, and audit-ready execution.

That makes it a stronger example of real enterprise AI thinking.

Future improvements

Add real authentication and user identity support

Store audit history in a database instead of CSV

Add notification support for escalations and approvals

Add report generation in PDF format

Add stronger role based production controls

Add deployment configuration for cloud hosting

Add more realistic SAP FICO style input data

Add LLM based narrative summaries for deeper business explanation 

Author
Ashok Ajmeera
