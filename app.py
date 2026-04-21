import streamlit as st
import scanner  # This imports your working Phase 1 engine!

# --- UI Configuration ---
st.set_page_config(page_title="CodeShield DLP", page_icon="🛡️", layout="wide")

# --- HIDE STREAMLIT BRANDING ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("🛡️ CodeShield")
st.markdown("### Data Loss Prevention Engine")
st.markdown("Detect and redact sensitive secrets, API keys, and credentials from your codebase before pushing to production.")

st.divider()

# --- Input Section ---
st.subheader("1. Input Source")
input_method = st.radio("Choose input method:", ("Paste Text/Code", "Upload .txt or .py File"))

raw_data = ""

if input_method == "Paste Text/Code":
    raw_data = st.text_area("Paste your code here:", height=250)
else:
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "py", "json", "env"])
    if uploaded_file is not None:
        raw_data = uploaded_file.getvalue().decode("utf-8")
        st.code(raw_data, language="python") # Quick preview of what they uploaded

# --- Action Section ---
st.write("") # Spacer
if st.button("Scan for Vulnerabilities", type="primary", use_container_width=True):
    if not raw_data.strip():
        st.warning("Please provide some code or text to scan.")
    else:
        with st.spinner("Analyzing code against threat signatures..."):
            try:
                # --- THIS IS WHERE YOUR ENGINE RUNS ---
                results = scanner.scan_code_for_secrets(raw_data)
                
                st.success("Scan Complete!")
                st.divider()

                # --- Results: Threat Summary ---
                st.subheader("📊 Threat Summary")
                threats = results.get("threat_summary", [])
                
                if not threats:
                    st.info("✅ No sensitive data or secrets detected. Code is clean.")
                else:
                    # Create a modern grid of metric cards
                    cols = st.columns(len(threats))
                    for i, threat in enumerate(threats):
                        with cols[i]:
                            severity = threat.get('severity', 'UNKNOWN')
                            count = threat.get('count', 0)
                            type_name = threat.get('type', 'Unknown Threat')
                            
                            # Streamlit boxes color-coded by severity
                            if severity == "CRITICAL":
                                st.error(f"**{severity}**\n\n{type_name}: {count} found")
                            elif severity == "HIGH":
                                st.warning(f"**{severity}**\n\n{type_name}: {count} found")
                            else:
                                st.info(f"**{severity}**\n\n{type_name}: {count} found")

                st.write("") # Spacer

                # --- Results: Sanitized Code ---
                st.subheader("🔒 Sanitized Output")
                st.markdown("All detected secrets have been stripped and replaced with `[REDACTED]`.")
                st.code(results.get("sanitized_code", ""), language="python")

            except Exception as e:
                st.error(f"An engine error occurred: {e}")