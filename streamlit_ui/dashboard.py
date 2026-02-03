import json
import streamlit as st

from src.model_adapter import analyze_contract
from src.logger import save_run

st.set_page_config(page_title="GenAI Contract Risk Analyzer", layout="wide")

st.title("GenAI Contract Risk Analyzer (Portfolio Demo)")
st.caption("Enterprise-style outputs: data contract, evidence, audit log, and exportable JSON.")

# --- Input section ---
left, right = st.columns([1.05, 0.95])

with left:
    st.subheader("1) Provide contract text")

    input_type = st.radio("Input type", ["Paste text", "Upload .txt"], horizontal=True)
    contract_title = st.text_input("Contract title", value="Sample MSA")

    contract_text = ""
    source_type = "paste"

    if input_type == "Paste text":
        contract_text = st.text_area("Paste contract here", height=320)
        source_type = "paste"
    else:
        uploaded = st.file_uploader("Upload .txt contract", type=["txt"])
        if uploaded is not None:
            contract_text = uploaded.read().decode("utf-8", errors="ignore")
            source_type = "upload"
            st.success("File loaded successfully.")

    run_btn = st.button("Analyze contract", type="primary", disabled=(len(contract_text.strip()) == 0))

with right:
    st.subheader("2) Output")
    if "result" not in st.session_state:
        st.info("Run analysis to see results here.")

# --- Run analysis ---
if run_btn:
    result_obj = analyze_contract(contract_text, title=contract_title, source_type=source_type)

    # Convert to dict for rendering + download
    result = result_obj.model_dump()
    st.session_state["result"] = result

    # Save audit log to /logs
    save_run(result["run_id"], result)

# --- Render results ---
if "result" in st.session_state:
    data = st.session_state["result"]

    # Summary metrics (these are the first thing a hiring manager sees)
    m1, m2, m3 = st.columns(3)
    m1.metric("Overall Risk Score", data["summary"]["overall_risk_score"])
    m2.metric("Risk Level", data["summary"]["risk_level"])
    m3.metric("Findings", len(data["findings"]))

    st.divider()

    # Tabs: Findings / Evidence / Features / Scoring / Audit / Data Contract
    tab1, tab2, tab_feat, tab_score, tab3, tab4 = st.tabs(
        ["Risk Register", "Evidence", "Features Extracted", "Scoring Logic", "Audit Log", "Data Contract"]
    )

    with tab1:
        st.subheader("Risk Register")
        if len(data["findings"]) == 0:
            st.warning("No findings returned.")
        else:
            for f in data["findings"]:
                title = f'{f["finding_id"]} | {f["category"]} | {f["severity"]}'
                with st.expander(title, expanded=False):
                    st.write("**Risk statement:**", f["risk_statement"])
                    st.write("**Recommendation:**", f["recommendation"])
                    if f.get("proposed_redline"):
                        st.write("**Proposed redline:**", f["proposed_redline"])
                    st.write("**Confidence:**", f["confidence"])

    with tab2:
        st.subheader("Evidence (No claim without clause snippet)")
        if len(data["findings"]) == 0:
            st.info("Run analysis first.")
        else:
            ids = [f["finding_id"] for f in data["findings"]]
            selected = st.selectbox("Select a finding", options=ids)

            finding = next(x for x in data["findings"] if x["finding_id"] == selected)
            ev = finding.get("evidence", [])

            if not ev:
                st.error("Evidence missing — needs review.")
            else:
                for e in ev:
                    st.write(f'**{e["clause_ref"]}**')
                    st.code(e["snippet"])

    with tab_feat:
        st.subheader("Features Extracted (DS handshake layer)")
        feats = (data.get("features") or {}).get("features", [])
        if not feats:
            st.info("No features returned.")
        else:
            # Nice table for leadership + DS
            rows = [{"name": f["name"], "value": f["value"], "dtype": f["dtype"]} for f in feats]
            st.dataframe(rows, use_container_width=True)

            st.caption(
                "These features are the structured inputs you would typically hand off to a DS model "
                "(classifier/regression) or use for monitoring."
            )

    with tab_score:
        st.subheader("Scoring Logic (transparent + reviewable)")
        scoring = data.get("scoring")
        if not scoring:
            st.info("No scoring breakdown returned.")
        else:
            st.write("**Method:**", scoring.get("method"))
            st.write("**Weights:**", scoring.get("weights"))
            st.write("**Total points:**", scoring.get("total_points"))
            st.write("**Normalized score (0–100):**", scoring.get("normalized_score_0_100"))
            st.write("**Risk level:**", scoring.get("risk_level"))

            st.divider()
            st.subheader("Per-finding breakdown")
            items = scoring.get("items", [])
            if items:
                st.dataframe(items, use_container_width=True)
            else:
                st.info("No items in scoring breakdown.")

    with tab3:
        st.subheader("Audit Log")
        st.json(data.get("audit", []))

        st.subheader("Download JSON")
        st.download_button(
            label="Download analysis.json",
            data=json.dumps(data, indent=2),
            file_name="analysis.json",
            mime="application/json",
        )

    with tab4:
        st.subheader("Data + Model Interface Contract (what engineers care about)")
        st.markdown(
            """
**Input**
- `contract_text` (string)
- `title` (string)
- `source_type` (`paste|upload`)

**Output**
- `run_id` (string)
- `summary` (risk score + level + top risks)
- `findings[]` (structured risk register)
- `features` (feature set for DS/modeling)
- `scoring` (explainable breakdown: weights + points)
- `audit[]` events

**Evidence rule**
- No finding is valid unless it has at least one evidence snippet.
            """
        )