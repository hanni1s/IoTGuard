import streamlit as st
import pandas as pd
import sys
import os
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- Path setup for imports ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import get_scan_history, get_technician_alerts, get_unread_alert_count, mark_alert_as_read, mark_all_alerts_as_read

# --- Page Configuration ---
st.set_page_config(page_title="Technician Dashboard", layout="wide", initial_sidebar_state="collapsed")

# ------------------ ENHANCED CUSTOM CSS ------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: white;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stat-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 25px;
        margin: 10px 0;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stat-number {
        font-size: 42px;
        font-weight: 700;
        margin: 10px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        font-size: 13px;
        color: rgba(255, 255, 255, 0.7);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 30px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px 0 rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px 0 rgba(102, 126, 234, 0.6) !important;
    }
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 10px !important;
    }
    
    .stRadio > div {
        background: rgba(255, 255, 255, 0.05);
        padding: 10px 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .dataframe {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
    }
    
    .js-plotly-plot {
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.03);
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    h1, h2, h3 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        margin: 30px 0;
    }
    
    .stAlert {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        border-left: 4px solid !important;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #27ae60 0%, #229954 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 12px 25px !important;
        font-weight: 600 !important;
    }
    
    .insight-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .insight-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(102, 126, 234, 0.5);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: rgba(255, 255, 255, 0.6);
        border-radius: 10px;
        padding: 12px 25px;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.05);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Particle Animation */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
    }
    
    .particle {
        position: absolute;
        background: rgba(255, 255, 255, 0.7);
        border-radius: 50%;
        animation: float linear infinite;
    }
    
    @keyframes float {
        0% {
            transform: translateY(100vh) translateX(0);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100vh) translateX(100px);
            opacity: 0;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Add particle effects
st.markdown("""
    <div class="particles">
        <div class="particle" style="width: 5px; height: 5px; left: 8%; animation-duration: 20s; animation-delay: 0s;"></div>
        <div class="particle" style="width: 3px; height: 3px; left: 15%; animation-duration: 16s; animation-delay: 3s;"></div>
        <div class="particle" style="width: 4px; height: 4px; left: 25%; animation-duration: 22s; animation-delay: 6s;"></div>
        <div class="particle" style="width: 6px; height: 6px; left: 35%; animation-duration: 18s; animation-delay: 2s;"></div>
        <div class="particle" style="width: 3px; height: 3px; left: 42%; animation-duration: 24s; animation-delay: 8s;"></div>
        <div class="particle" style="width: 5px; height: 5px; left: 52%; animation-duration: 19s; animation-delay: 4s;"></div>
        <div class="particle" style="width: 4px; height: 4px; left: 63%; animation-duration: 21s; animation-delay: 7s;"></div>
        <div class="particle" style="width: 3px; height: 3px; left: 72%; animation-duration: 17s; animation-delay: 1s;"></div>
        <div class="particle" style="width: 5px; height: 5px; left: 82%; animation-duration: 23s; animation-delay: 5s;"></div>
        <div class="particle" style="width: 4px; height: 4px; left: 92%; animation-duration: 20s; animation-delay: 9s;"></div>
    </div>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("""
    <div style='
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    '>
        <h1 style='color: white; text-align: center; margin: 0; font-size: 42px; -webkit-text-fill-color: white;'>
            IoTGuard Technician Dashboard
        </h1>
        <p style='color: rgba(255,255,255,0.9); text-align: center; margin: 10px 0 0 0; font-size: 16px;'>
            Advanced Analytics & Network Monitoring System
        </p>
    </div>
""", unsafe_allow_html=True)

# ------------------ TOP BAR ------------------
col1, col2 = st.columns([3, 1])

with col1:
    username = st.session_state.get("username", "Technician")
    st.markdown(f"""
        <div style='
            background: rgba(255, 255, 255, 0.05);
            padding: 15px 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        '>
            <span style='font-size: 14px; color: rgba(255,255,255,0.7);'>Logged in as</span><br>
            <span style='font-size: 20px; font-weight: 600; color: white;'>{username}</span>
        </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("Logout", key="logout_btn"):
        st.session_state.clear()
        st.switch_page("main.py")

st.markdown("<br>", unsafe_allow_html=True)

# ------------------ LOAD DATA ------------------
data = get_scan_history()

if data:
    df = pd.DataFrame(
        data,
        columns=["ID", "Username", "Target IP", "Open Ports", "Risk Summary", "Date", "AI Prediction"]
    )
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # ------------------ TABS ------------------
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "AI Intelligence", "Scan Records", "Security Alerts"])

    # ==========================================
    # TAB 1: OVERVIEW
    # ==========================================
    with tab1:
        st.markdown("### Network Security Overview")
        
        # Summary Cards
        total_scans = len(df)
        high_count = df[df["AI Prediction"].str.contains("High", case=False, na=False)].shape[0]
        medium_count = df[df["AI Prediction"].str.contains("Medium", case=False, na=False)].shape[0]
        low_count = df[df["AI Prediction"].str.contains("Low", case=False, na=False)].shape[0]
        unique_users = df["Username"].nunique()

        card1, card2, card3, card4, card5 = st.columns(5)

        with card1:
            st.markdown(f"""
                <div class='stat-card'>
                    <div class='stat-label'>Total Scans</div>
                    <div class='stat-number'>{total_scans}</div>
                    <div style='color: rgba(255,255,255,0.5); font-size: 12px;'>All time</div>
                </div>
            """, unsafe_allow_html=True)

        with card2:
            st.markdown(f"""
                <div class='stat-card'>
                    <div class='stat-label'>High Risk</div>
                    <div class='stat-number' style='background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); -webkit-background-clip: text;'>{high_count}</div>
                    <div style='color: rgba(255,255,255,0.5); font-size: 12px;'>🔴 Critical</div>
                </div>
            """, unsafe_allow_html=True)

        with card3:
            st.markdown(f"""
                <div class='stat-card'>
                    <div class='stat-label'>Medium Risk</div>
                    <div class='stat-number' style='background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); -webkit-background-clip: text;'>{medium_count}</div>
                    <div style='color: rgba(255,255,255,0.5); font-size: 12px;'>🟠 Review</div>
                </div>
            """, unsafe_allow_html=True)

        with card4:
            st.markdown(f"""
                <div class='stat-card'>
                    <div class='stat-label'>Low Risk</div>
                    <div class='stat-number' style='background: linear-gradient(135deg, #27ae60 0%, #229954 100%); -webkit-background-clip: text;'>{low_count}</div>
                    <div style='color: rgba(255,255,255,0.5); font-size: 12px;'>🟢 Secure</div>
                </div>
            """, unsafe_allow_html=True)

        with card5:
            st.markdown(f"""
                <div class='stat-card'>
                    <div class='stat-label'>Active Users</div>
                    <div class='stat-number' style='background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); -webkit-background-clip: text;'>{unique_users}</div>
                    <div style='color: rgba(255,255,255,0.5); font-size: 12px;'>👥 Accounts</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # Visualizations
        st.markdown("### Analytics")

        viz_col1, viz_col2 = st.columns(2)

        with viz_col1:
            st.markdown("#### Risk Distribution")
            fig_risk = px.pie(
                df,
                names="AI Prediction",
                color="AI Prediction",
                color_discrete_map={
                    "High Risk": "#e74c3c",
                    "Medium Risk": "#f39c12",
                    "Low Risk": "#27ae60"
                },
                hole=0.4
            )
            fig_risk.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                height=350
            )
            st.plotly_chart(fig_risk, use_container_width=True)

        with viz_col2:
            st.markdown("#### Scans Over Time")
            time_data = df.groupby(df["Date"].dt.date).size().reset_index(name="Count")
            fig_time = px.line(time_data, x="Date", y="Count", markers=True)
            fig_time.update_traces(line_color='#667eea', line_width=3, marker=dict(size=8))
            fig_time.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                height=350
            )
            st.plotly_chart(fig_time, use_container_width=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # Smart Insights
        st.markdown("### Smart Insights")
        
        top_user = df["Username"].value_counts().idxmax()
        top_user_scans = df["Username"].value_counts().max()
        top_ip = df["Target IP"].value_counts().idxmax()
        top_ip_count = df["Target IP"].value_counts().max()
        
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
                <div class='insight-card'>
                    <h4 style='color: white; margin: 0; -webkit-text-fill-color: white;'>👤 Top User</h4>
                    <p style='font-size: 24px; font-weight: 700; color: #667eea; margin: 10px 0;'>{top_user}</p>
                    <p style='color: rgba(255,255,255,0.6); font-size: 14px; margin: 0;'>{top_user_scans} scans</p>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class='insight-card'>
                    <h4 style='color: white; margin: 0; -webkit-text-fill-color: white;'>Most Scanned</h4>
                    <p style='font-size: 20px; font-weight: 700; color: #667eea; margin: 10px 0;'>{top_ip}</p>
                    <p style='color: rgba(255,255,255,0.6); font-size: 14px; margin: 0;'>{top_ip_count} times</p>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            risk_pct = round((high_count / total_scans) * 100, 1) if total_scans > 0 else 0
            st.markdown(f"""
                <div class='insight-card'>
                    <h4 style='color: white; margin: 0; -webkit-text-fill-color: white;'>Risk Rate</h4>
                    <p style='font-size: 24px; font-weight: 700; color: #e74c3c; margin: 10px 0;'>{risk_pct}%</p>
                    <p style='color: rgba(255,255,255,0.6); font-size: 14px; margin: 0;'>High risk ratio</p>
                </div>
            """, unsafe_allow_html=True)

        with col4:
            latest = df.sort_values("Date", ascending=False).iloc[0]
            latest_emoji = "🔴" if "High" in str(latest["AI Prediction"]) else ("🟠" if "Medium" in str(latest["AI Prediction"]) else "🟢")
            st.markdown(f"""
                <div class='insight-card'>
                    <h4 style='color: white; margin: 0; -webkit-text-fill-color: white;'>Latest</h4>
                    <p style='font-size: 32px; margin: 10px 0;'>{latest_emoji}</p>
                    <p style='color: rgba(255,255,255,0.6); font-size: 14px; margin: 0;'>{latest["Date"].strftime("%m/%d %H:%M")}</p>
                </div>
            """, unsafe_allow_html=True)

    # ==========================================
    # TAB 2: AI INTELLIGENCE
    # ==========================================
    with tab2:
        st.markdown("### AI Risk Intelligence & Predictions")
        st.write("Advanced predictive analytics for IoT vulnerabilities")
        st.markdown("<hr>", unsafe_allow_html=True)

        # AI Summary Cards
        ai_col1, ai_col2, ai_col3, ai_col4 = st.columns(4)
        
        ai_col1.metric("Total Scans Analyzed", total_scans)
        ai_col2.metric("🔴 High Risk Detected", high_count)
        ai_col3.metric("🟠 Medium Risk Detected", medium_count)
        ai_col4.metric("🟢 Low Risk Detected", low_count)

        st.markdown("<hr>", unsafe_allow_html=True)

        # Risk Trend Analysis
        st.markdown("#### Risk Trend Over Time")
        trend_data = df.groupby([pd.Grouper(key="Date", freq="W"), "AI Prediction"]).size().reset_index(name="Count")
        
        fig_trend = px.line(
            trend_data,
            x="Date",
            y="Count",
            color="AI Prediction",
            markers=True,
            color_discrete_map={
                "High Risk": "#e74c3c",
                "Medium Risk": "#f39c12",
                "Low Risk": "#27ae60"
            }
        )
        fig_trend.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            height=400
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # AI Predictions
        st.markdown("#### Next Week Risk Forecast")

        # Check if we have enough data for predictions
        has_sufficient_data = any(len(trend_data[trend_data["AI Prediction"] == risk]) > 2 
                                  for risk in ["High Risk", "Medium Risk", "Low Risk"])

        if not has_sufficient_data:
            st.info("""
            **Predictive Analytics Requires Historical Data**
    
            To generate accurate risk forecasts, the system needs at least 3 weeks of scan history.
    
            **Current Status:** Collecting baseline data...  
            **Next Steps:** Perform regular scans to enable trend predictions and proactive risk planning.
            """)

        predictions = []
        for risk in ["High Risk", "Medium Risk", "Low Risk"]:
            subset = trend_data[trend_data["AI Prediction"] == risk]
            if len(subset) > 2:
                x = np.arange(len(subset))
                y = subset["Count"].values
                slope, intercept = np.polyfit(x, y, 1)
                next_week = slope * len(subset) + intercept
                next_week = max(0, round(next_week))
                predictions.append({"Risk Level": risk, "Predicted Count": next_week})
            else:
                predictions.append({"Risk Level": risk, "Predicted Count": "Insufficient data"})

        pred_df = pd.DataFrame(predictions)
        st.dataframe(pred_df, use_container_width=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # Top Vulnerable Devices
        st.markdown("#### Top 5 Most Vulnerable Devices")
        
        high_risk_df = df[df["AI Prediction"].str.contains("High", case=False, na=False)]
        if not high_risk_df.empty:
            top_devices = high_risk_df["Target IP"].value_counts().head(5).reset_index()
            top_devices.columns = ["Target IP", "High Risk Count"]
            
            fig_bar = px.bar(
                top_devices,
                x="Target IP",
                y="High Risk Count",
                color="High Risk Count",
                color_continuous_scale="Reds"
            )
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                height=400
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No high-risk devices detected yet.")

        st.markdown("<hr>", unsafe_allow_html=True)

        # AI Insights
        st.markdown("#### AI-Generated Insights")
        
        if high_count > medium_count and high_count > low_count:
            st.error("🔴 **Network Status: High Risk** — Immediate security review recommended")
        elif medium_count > high_count:
            st.warning("🟠 **Network Status: Moderate Risk** — Continue monitoring and apply patches")
        else:
            st.success("🟢 **Network Status: Low Risk** — Security posture is healthy")

        st.info("**Tip:** Predictions are based on historical trends using linear regression analysis")

    # ==========================================
    # TAB 3: SCAN RECORDS
    # ==========================================
    with tab3:
        st.markdown("### Detailed Scan Records")
        
        # Filter Panel
        with st.expander("Advanced Filters", expanded=True):
            fcol1, fcol2, fcol3 = st.columns(3)

            min_date, max_date = df["Date"].min(), df["Date"].max()
            date_input = fcol1.date_input("Date Range", value=(min_date, max_date))

            if isinstance(date_input, tuple) and len(date_input) == 2:
                start_date, end_date = date_input
            else:
                start_date, end_date = min_date, max_date

            risk_levels = df["AI Prediction"].dropna().unique().tolist()
            selected_risks = fcol2.multiselect("Risk Levels", options=risk_levels, default=risk_levels)
            search_term = fcol3.text_input("Search", placeholder="Username or IP...")

            if st.button("Reset Filters"):
                st.rerun()

        # Apply Filters
        mask = (df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))
        if selected_risks:
            mask &= df["AI Prediction"].isin(selected_risks)
        if search_term:
            mask &= (df["Username"].str.contains(search_term, case=False, na=False) | 
                     df["Target IP"].str.contains(search_term, case=False, na=False))
        
        filtered_df = df[mask]

        st.info(f"Showing {len(filtered_df)} of {total_scans} total scans")

        # Data Table
        st.dataframe(filtered_df, use_container_width=True, height=500)

        # Download
        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Filtered Data (CSV)",
            data=csv,
            file_name="iotguard_scan_records.csv",
            mime="text/csv"
        )
    
    # ==========================================
    # TAB 4: SECURITY ALERTS
    # ==========================================
    with tab4:
        st.markdown("### Security Alerts")
        st.write("Real-time notifications of high-risk devices detected by users")
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Filter options
        col1, col2 = st.columns([3, 1])
        
        with col1:
            filter_option = st.radio(
                "Filter:",
                ["All Alerts", "Unread Only"],
                horizontal=True
            )
        
        with col2:
            if st.button("✅ Mark All Read"):
                mark_all_alerts_as_read()
                st.success("All alerts marked as read!")
                st.rerun()
        
        # Get alerts
        if filter_option == "Unread Only":
            alerts = get_technician_alerts(unread_only=True)
        else:
            alerts = get_technician_alerts(unread_only=False)
        
        # Display alerts
        if alerts:
            st.info(f"{len(alerts)} alert(s) found")
            
            for alert in alerts:
                alert_id, username, target_ip, risk_level, high_risk_ports, port_details, alert_message, created_at, is_read, scan_id = alert
                
                # Color coding based on risk
                if "High" in risk_level:
                    icon, bg_color, border_color = "🔴", "rgba(231, 76, 60, 0.1)", "#e74c3c"
                elif "Medium" in risk_level:
                    icon, bg_color, border_color = "🟠", "rgba(243, 156, 18, 0.1)", "#f39c12"
                else:
                    icon, bg_color, border_color = "🟢", "rgba(39, 174, 96, 0.1)", "#27ae60"
                
                read_badge = "🔴 NEW" if is_read == 0 else "✅ Read"
                
                # Alert card
                st.markdown(f"""
                    <div style='
                        background: {bg_color};
                        border-left: 5px solid {border_color};
                        padding: 20px;
                        border-radius: 10px;
                        margin: 15px 0;
                        backdrop-filter: blur(10px);
                    '>
                        <h4 style='margin: 0; color: white; -webkit-text-fill-color: white;'>
                            {icon} {risk_level.upper()} ALERT
                        </h4>
                        <p style='margin: 8px 0 0 0; font-size: 13px; color: rgba(255,255,255,0.6);'>
                            {created_at} | {read_badge}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Details in expander
                with st.expander("View Alert Details"):
                    detail_col1, detail_col2 = st.columns(2)
                    
                    with detail_col1:
                        st.write(f"**User:** {username}")
                        st.write(f"**Device IP:** {target_ip}")
                        st.write(f"**Risk Level:** {risk_level}")
                    
                    with detail_col2:
                        st.write(f"**Scan ID:** {scan_id}")
                        st.write(f"**Status:** {'Unread' if is_read == 0 else 'Read'}")
                        st.write(f"**Detected:** {created_at}")
                    
                    st.markdown("---")
                    st.markdown("**Critical Ports Detected:**")
                    st.write(f"**Ports:** {high_risk_ports}")
                    
                    st.markdown("**Vulnerability Details:**")
                    # Parse and display port details nicely
                    if port_details:
                        details_list = port_details.split(" | ")
                        for detail in details_list:
                            st.write(f"• {detail}")
                    
                    st.markdown("---")
                    
                    # Action buttons
                    btn_col1, btn_col2 = st.columns(2)
                    
                    with btn_col1:
                        if is_read == 0:
                            if st.button(f"Mark as Read", key=f"read_{alert_id}"):
                                mark_alert_as_read(alert_id)
                                st.success("Alert marked as read!")
                                st.rerun()
                    
                    with btn_col2:
                        st.info(f"Recommended: Contact user **{username}** to remediate vulnerabilities")
        
        else:
            st.success("✅ No alerts! All systems secure.")

else:
    st.info("No scan data available. Perform scans to populate analytics.")


# ------------------ FOOTER ------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; padding: 20px; color: rgba(255,255,255,0.5);'>
        <p style='margin: 0; font-size: 13px;'>
            IoTGuard &copy; 2025 | Advanced IoT Security Platform
        </p>
        <p style='margin: 5px 0 0 0; font-size: 11px;'>
            Powered by AI | Protecting IoT Infrastructure Worldwide
        </p>
    </div>
""", unsafe_allow_html=True)