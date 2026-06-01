import streamlit as st
import requests

# 1. Page Configuration (Sets up a clean, wide tech-dashboard look)
st.set_page_config(
    page_title="CodeShield AI | Security Audit",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ CodeShield AI Source Auditor")
st.subheader("Real-time static code analysis & secret redaction powered by FastAPI")

# 2. Sidebar Information
with st.sidebar:
    st.header("System Status")
    st.success("Frontend: Active (Port 8501)")
    st.info("Target Backend: http://127.0.0.1:8000/scan")
    st.markdown("---")
    st.markdown("### Rules Enabled:")
    st.markdown("- [x] API Key Detection\n- [x] Password Scanning\n- [x] Automated Redaction")

# 3. Input Layout
st.markdown("### Paste Source Code for Security Audit")
user_code = st.text_area(
    label="Supports Python, JavaScript, configuration files, and environment variables",
    value="# Paste your code here to scan for leaked credentials...\n",
    height=250
)

# 4. Trigger Button
if st.button("🚀 Execute Security Scan", type="primary"):
    if not user_code.strip() or user_code.startswith("# Paste your code here"):
        st.warning("Please provide valid source code to audit.")
    else:
        # Create a visual loading indicator while waiting for the FastAPI server
        with st.spinner("Streaming payload to FastAPI backend & processing via Gemini API..."):
            try:
                # Pack the text into the strict JSON structure the Pydantic model requires
                payload = {"raw_code": user_code}
                
                # Make the live HTTP POST request to your running backend
                response = requests.post(
                    "http://127.0.0.1:8000/scan", 
                    json=payload,
                    timeout=30
                )
                
                # Check if the bouncer let us through (200 OK)
                if response.status_code == 200:
                    result = response.json()
                    st.balloons()
                    
                    st.markdown("---")
                    st.success("📊 Audit Complete! Security report generated successfully.")
                    
                    # Split screen layout into columns to show original vs sanitized code cleanly
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 🔴 Analyzed Code")
                        st.code(user_code, language="python")
                        
                    with col2:
                        st.markdown("#### 🟢 Sanitized Output")
                        # Extracts the sanitized code returned by your FastAPI endpoint
                        sanitized = result.get("sanitized_code", "No code returned.")
                        st.code(sanitized, language="python")
                        
                    # Display the deep breakdown report at the bottom
                    st.markdown("### 📋 AI Security Vulnerability Report")
                    report_text = result.get("threat_report", "No report details provided.")
                    st.info(report_text)
                    
                elif response.status_code == 422:
                    st.error("❌ Backend rejected the format (422 Unprocessable Content). Check your data structure.")
                else:
                    st.error(f"❌ Backend Error: Server responded with status code {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("🚨 Connection Failed! Is your FastAPI server running on http://127.0.0.1:8000? Run 'fastapi dev api.py' in a separate terminal.")