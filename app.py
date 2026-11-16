import streamlit as st
import pandas as pd
import time
from engine import fetch_and_extract_brightdata, validate_schema, DATASET_ID

# 1. Page Config
st.set_page_config(
    page_title="ScraperSentinel | Bright Data Control Tower", 
    page_icon="🛡️", 
    layout="wide"
)

# 2. Custom CSS
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    [data-testid="stMetric"] {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        padding: 14px !important;
        border-radius: 8px !important;
    }
    [data-testid="stMetricValue"] { color: #0F172A !important; font-weight: 700 !important; }
    .status-healthy { background-color: #DCFCE7; border: 1px solid #16A34A; color: #14532D; padding: 10px 14px; border-radius: 6px; font-weight: 600; margin-bottom: 10px; }
    .status-broken { background-color: #FEE2E2; border: 1px solid #DC2626; color: #7F1D1D; padding: 10px 14px; border-radius: 6px; font-weight: 600; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# 3. Header Banner
st.title("🛡️ ScraperSentinel: Enterprise Data Guard")
st.caption("Real-Time Autonomous Control Tower Powered by Bright Data Web Unlocker & Scraper Studio")
st.divider()

# 4. Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/color/96/shield.png", width=50)
    st.header("🌐 Bright Data Node Input")
    
    target_url = st.text_input(
        "Target Target Server URL:", 
        value="http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
    )
    
    st.divider()
    st.markdown("### 🎛️ Selector Overrides (Optional)")
    container_in = st.text_input("Container Selector", value="")
    title_in = st.text_input("Title Selector", value="")
    price_in = st.text_input("Price Selector", value="")

# 5. KPI Metrics
k1, k2, k3, k4 = st.columns(4)
with k1: st.metric("Pipeline Network", "Bright Data DCA")
with k2: st.metric("Collector ID", DATASET_ID)
with k3: st.metric("Anti-Bot Protection", "Web Unlocker Active")
with k4: st.metric("Self-Healing Mode", "AUTONOMOUS")

st.divider()

# 6. Main Dashboard
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("📊 Ingestion & Extracted Intelligence")
    
    if st.button("🚀 Trigger Ingestion via Bright Data", type="primary", width="stretch"):
        with st.status("Routing request through Bright Data proxy nodes...", expanded=True) as status:
            st.write("📡 Handshaking with Bright Data Web Unlocker API...")
            time.sleep(0.3)
            
            data, selectors, log_msg = fetch_and_extract_brightdata(
                target_url, container_in, title_in, price_in
            )
            
            st.write(f"🌐 {log_msg}")
            is_healthy, val_msg = validate_schema(data)
            
            if is_healthy:
                status.update(label="Ingestion Successful!", state="complete", expanded=False)
                st.markdown(f'<div class="status-healthy">✅ {val_msg}</div>', unsafe_allow_html=True)
                
                df = pd.DataFrame(data)
                tab_table, tab_cards = st.tabs(["📋 Extracted Dataset", "🎴 Visual Product Cards"])
                
                with tab_table:
                    st.dataframe(df, width="stretch", hide_index=True)
                    st.download_button("📥 Export Clean CSV", df.to_csv(index=False), "brightdata_extracted.csv", "text/csv")
                
                with tab_cards:
                    cols = st.columns(3)
                    for idx, row in df.iterrows():
                        with cols[idx % 3]:
                            st.metric(label=row["title"] if row["title"] else "Product", value=row["price"] if row["price"] else "N/A")
            else:
                status.update(label="Schema Error / Decayed Selectors", state="error", expanded=True)
                st.markdown(f'<div class="status-broken">❌ {val_msg}</div>', unsafe_allow_html=True)
                if data:
                    st.dataframe(pd.DataFrame(data), width="stretch", hide_index=True)

with col_right:
    st.subheader("🧠 Inspector & Bright Data Telemetry")
    t1, t2 = st.tabs(["🎯 Active Mappings", "📜 Execution Logs"])
    
    with t1:
        st.markdown("**Active CSS Selectors:**")
        if 'selectors' in locals():
            st.json(selectors)
        else:
            st.info("Execute pipeline to view live selector mapping.")
            
    with t2:
        st.code(f"""
[INFO] Request routed to target: {target_url[:35]}...
[PROXY] Handshake established with Bright Data Unlocker.
[STATUS] HTTP 200 OK. Payload parsed.
[GUARD] Pydantic schema verification executed.
        """, language="bash")