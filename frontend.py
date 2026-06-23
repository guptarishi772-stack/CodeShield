import streamlit as st
import requests
import time

# --- CONFIGURATION ---
API_URL = "https://codeshield-api.onrender.com/scan"
st.set_page_config(page_title="CodeShield DLP", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS (Sleek UI tweaks) ---
st.markdown("""
    <style>
    /* Make the scan button massive and modern */
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { border-color: #ff4b4b; color: #ff4b4b; }
    /* Hide the default Streamlit top menu and footer for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Navigation & Status) ---
with st.sidebar:
    st.title("🛡️ CodeShield")
    st.caption("Enterprise Data Loss Prevention")
    st.divider()
    
    st.markdown("### System Status")
    # A pro-level trick: Ping the backend to see if it's alive
    try:
        requests.get("http://127.0.0.1:8000/docs", timeout=1)
        st.success("🟢 Backend Engine: **Online**")
    except requests.exceptions.ConnectionError:
        st.error("🔴 Backend Engine: **Offline**")
        st.caption("Run `fastapi dev api.py` in your terminal.")
    
    st.divider()
    st.markdown("**Version:** 2.0.0 (Microservice)")
    st.markdown("**Local Database:** SQLite Active")

# --- MAIN DASHBOARD ---
st.title("CodeShield Security Scanner")
st.markdown("Detect hardcoded secrets, API keys, and critical vulnerabilities before they hit production.")

# --- INPUT SECTION (Modern Tabs) ---
tab1, tab2 = st.tabs(["💻 Paste Source Code", "📁 Upload File"])

code_to_scan = ""

with tab1:
    manual_code = st.text_area("Enter Python, JSON, or generic text:", height=250, placeholder="import requests\napi_key = 'sk-12345...'")
    if manual_code:
        code_to_scan = manual_code

with tab2:
    # Accept multiple file types
    uploaded_file = st.file_uploader("Upload a source file for deep scanning", type=["py", "txt", "env", "json"])
    if uploaded_file is not None:
        # Decode the uploaded file into a text string
        string_data = uploaded_file.getvalue().decode("utf-8")
        st.info(f"File '{uploaded_file.name}' loaded successfully.")
        with st.expander("Preview Uploaded Code"):
            st.code(string_data[:500] + ("\n...[truncated]" if len(string_data) > 500 else ""), language="python")
        code_to_scan = string_data

# --- SCAN EXECUTION ---
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1]) # Centers the button

with col2:
    analyze_button = st.button("🚀 Run Vulnerability Scan", type="primary", use_container_width=True)

if analyze_button:
    if not code_to_scan.strip():
        st.warning("⚠️ Please provide code or upload a file to scan.")
    else:
        # A beautiful animated loading sequence
        with st.status("Initializing CodeShield Engine...", expanded=True) as status:
            st.write("Packaging payload...")
            time.sleep(0.3) # Purely for visual polish
            st.write("Connecting to FastAPI Backend...")
            
            payload = {"raw_code": code_to_scan}
            
            try:
                # Send the data to your API engine
                response = requests.post(API_URL, json=payload, timeout=30)
                response.raise_for_status() # Trigger error if status code is not 200
                report = response.json()
                
                status.update(label="Scan Complete!", state="complete", expanded=False)
                
                # --- RESULTS DASHBOARD ---
                st.divider()
                st.subheader("📊 Threat Intelligence Report")
                
                threats = report.get("threat_summary", [])
                
                # Logic: Did we find secrets, or did the engine crash?
                if not threats:
                    # THE FIX: Catch the silent failure!
                    if "Error" in report.get("sanitized_code", ""):
                        st.error("⚠️ **SCAN ABORTED:** The AI engine failed to process the code (Google API Overload). Do not trust this result.")
                        with st.expander("View Error Log"):
                            st.code(report.get("sanitized_code", ""), language="text")
                    else:
                        st.success("✅ **CLEAN:** No hardcoded secrets or vulnerabilities detected.")
                        with st.expander("View Sanitized Code"):
                            st.code(report.get("sanitized_code", ""), language="python")
                else:
                    # Metrics Display
                    m1, m2 = st.columns(2)
                    m1.metric(label="Critical Secrets Found", value=len(threats))
                    m2.metric(label="System Risk Level", value="HIGH", delta="- Immediate Action Required", delta_color="inverse")
                    
                    st.error("🚨 **CRITICAL THREATS DETECTED:** Secrets must be removed before deployment.")
                    
                    # Threat Breakdown Loop
                    st.markdown("### 🔍 Vulnerability Breakdown")
                    for i, threat in enumerate(threats):
                        with st.expander(f"Threat {i+1}: Click for details", expanded=True):
                            st.warning(threat)
                            
                    # Display the AI-Sanitized version of the code
                    with st.expander("🛡️ View Sanitized Code (Safe to Deploy)", expanded=True):
                        st.info("The following code has had its secrets redacted by the AI engine.")
                        st.code(report.get("sanitized_code", ""), language="python")
                        
            # --- ENTERPRISE ERROR HANDLING ---
            except requests.exceptions.ConnectionError:
                status.update(label="Engine Disconnected", state="error", expanded=False)
                st.error("🚨 **Connection Refused:** Cannot reach the FastAPI backend. Make sure your server is running!")
            except requests.exceptions.HTTPError as e:
                status.update(label="Scan Failed", state="error", expanded=False)
                if response.status_code == 503:
                    st.error("⚠️ **AI Engine Overloaded:** Google's Gemini API is experiencing high traffic. (Error 503). Your backend safely caught this error.")
                else:
                    st.error(f"🚨 **Backend Error:** The server returned a {response.status_code} error.")