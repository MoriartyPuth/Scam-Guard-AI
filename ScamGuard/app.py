import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import time
from core_engine import ScamGuardEngine
from data_generator import generate_live_data

# --- Setup ---
st.set_page_config(page_title="ScamGuard Pro", layout="wide", page_icon="🛡️")
engine = ScamGuardEngine()

# --- Custom Styling ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("🛡️ ScamGuard AI Panel")
data_size = st.sidebar.slider("Analysis Volume", 50, 500, 120)
risk_threshold = st.sidebar.slider("AI Sensitivity (Threshold)", 0.0, 1.0, 0.7)

# Initialize Data
df = generate_live_data(data_size)
engine.train_ai(df)
df['risk_score'] = df.apply(lambda r: engine.get_risk_score(r['amount'], r['time_gap_seconds']), axis=1)

# --- Dashboard Header ---
st.title("Financial Crime Analytics & Digital Flow")
st.write("Real-time scam pattern detection and automated fund tracking system.")

col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Total Scanned", len(df))
with col2: st.metric("High Risk", len(df[df['risk_score'] > risk_threshold]))
with col3: st.metric("Laundering Loops", "Calculating...")
with col4: st.metric("Status", "Live", delta="Shield Active")

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Money Flow Map", "🔄 Laundering Cycles", "🔍 Account Search", "🚨 Live Alerts"])

with tab1:
    st.subheader("Global Transaction Network")
    # Build graph using a subset for visual clarity
    G = engine.build_graph(df.head(40), risk_threshold)
    fig, ax = plt.subplots(figsize=(12, 7))
    pos = nx.spring_layout(G, k=0.5)
    
    edges = G.edges(data=True)
    edge_colors = ['red' if d['risk'] > risk_threshold else '#2ecc71' for u, v, d in edges]
    edge_widths = [3 if d['risk'] > risk_threshold else 1 for u, v, d in edges]

    nx.draw(G, pos, with_labels=True, node_color='#d5dbdb', edge_color=edge_colors, 
            width=edge_widths, arrowsize=25, node_size=1200, font_size=9, ax=ax)
    
    st.pyplot(fig)
    st.caption("Red lines indicate high-risk pathways detected by AI.")

with tab2:
    st.subheader("Circular Routing Detection")
    full_G = engine.build_graph(df, risk_threshold)
    cycles = engine.detect_laundering_cycles(full_G)
    
    if cycles:
        for c in cycles:
            st.error(f"⚠️ **LAUNDERING LOOP DETECTED**: {' ⮕ '.join(map(str, c))} ⮕ {c[0]}")
        st.info("These accounts are likely part of a 'wash trading' or 'layering' network.")
    else:
        st.success("No circular patterns detected in this dataset.")

with tab3:
    st.subheader("Account Deep-Dive")
    search_id = st.number_input("Enter Account ID (e.g., 999, 125)", min_value=0)
    if search_id:
        user_df = df[(df['sender'] == search_id) | (df['receiver'] == search_id)]
        if not user_df.empty:
            avg_risk = user_df['risk_score'].mean()
            st.write(f"**Risk Rating for #{search_id}:** {avg_risk:.2f}")
            st.progress(avg_risk)
            st.dataframe(user_df.sort_values('risk_score', ascending=False))
        else:
            st.warning("Account ID not found.")

with tab4:
    st.subheader("Simulate Real-Time Monitoring")
    if st.button("Initialize Stream"):
        alert_log = st.empty()
        for i in range(5):
            sample = df.sample(1).iloc[0]
            label, level = engine.trigger_alert_level(sample['risk_score'])
            
            if sample['risk_score'] > risk_threshold:
                st.toast(f"SUSPICIOUS ACTIVITY: ID {sample['tx_id']}", icon="🚨")
                st.write(f"[{time.strftime('%H:%M:%S')}] {label}: Transaction #{sample['tx_id']} flagged (Score: {sample['risk_score']:.2f})")
            time.sleep(1)

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.download_button("Export Forensic Report", df.to_csv().encode('utf-8'), "scam_audit.csv", "text/csv")