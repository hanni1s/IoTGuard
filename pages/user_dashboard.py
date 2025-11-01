import streamlit as st
import pandas as pd
import sys
import os
import re
from datetime import datetime

# --- Import path setup ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scan_module import scan_target, get_port_info_url
from report_module import generate_pdf, generate_csv, generate_json
from ai_model import predict_overall_risk
from database import save_scan_result, get_user_notifications, get_unread_count, mark_notification_as_read, mark_all_as_read, create_notification, get_scan_history
from evidence_collect import save_evidence

# ------------------ PAGE SETTINGS ------------------
st.set_page_config(page_title="User Dashboard", layout="wide", initial_sidebar_state="collapsed")

# ------------------ HIDE SIDEBAR COMPLETELY ------------------
st.markdown("""
    <style>
    /* Hide sidebar navigation */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Hide sidebar toggle button */
    button[kind="header"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ ENHANCED CUSTOM CSS ------------------
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container background */
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: white;
    }
    
    /* Card styling */
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
    
    /* Stat numbers */
    .stat-number {
        font-size: 36px;
        font-weight: 700;
        margin: 10px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        font-size: 14px;
        color: rgba(255, 255, 255, 0.7);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Alert boxes */
    .alert-box {
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        border-left: 5px solid;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .alert-high {
        background: rgba(231, 76, 60, 0.1);
        border-color: #e74c3c;
    }
    
    .alert-medium {
        background: rgba(243, 156, 18, 0.1);
        border-color: #f39c12;
    }
    
    .alert-low {
        background: rgba(39, 174, 96, 0.1);
        border-color: #27ae60;
    }
    
    /* Notification badge */
    .notification-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-left: 8px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.7;
        }
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px 0 rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(102, 126, 234, 0.6);
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        border-radius: 10px;
        padding: 12px;
    }
    
    /* Dataframe styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: rgba(255, 255, 255, 0.7);
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        margin: 30px 0;
    }
    
    /* Section headers */
    h1, h2, h3 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
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
        background: rgba(255, 255, 255, 0.8);
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

# ------------------ HELPER FUNCTION FOR IP VALIDATION ------------------
def is_valid_ip(ip):
    pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    if not ip or ip.strip() == "":
        return False, "IP address cannot be empty."
    if not re.match(pattern, ip.strip()):
        return False, "Invalid IP format. Please enter a valid IPv4 address (e.g., 192.168.1.1)"
    return True, ""

# ------------------ MODERN BRANDING HEADER ------------------
st.markdown("""
    <div style='
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    '>
        <h1 style='color: white; text-align: center; margin: 0; font-size: 42px; -webkit-text-fill-color: white;'>
            IoTGuard Security Dashboard
        </h1>
        <p style='color: rgba(255,255,255,0.9); text-align: center; margin: 10px 0 0 0; font-size: 16px;'>
            AI-Powered IoT Vulnerability Scanner | Advanced Threat Detection
        </p>
    </div>
""", unsafe_allow_html=True)

# ------------------ TOP BAR: User Info & Logout ------------------
username = st.session_state.get("username", "Unknown")
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown(f"""
        <div style='
            background: rgba(255, 255, 255, 0.05);
            padding: 15px 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        '>
            <span style='font-size: 14px; color: rgba(255,255,255,0.7);'>Logged in as</span><br>
            <span style='font-size: 20px; font-weight: 600; color: white;'>Hey! {username}</span>
        </div>
    """, unsafe_allow_html=True)

with col3:
    if st.button("Logout", key="logout_btn"):
        st.session_state.clear()
        st.switch_page("main.py")

st.markdown("<br>", unsafe_allow_html=True)

# ------------------ QUICK STATS DASHBOARD ------------------
scan_history = get_scan_history()
total_scans = len(scan_history)
unread_count = get_unread_count(username)

# Get user's scans only
user_scans = [s for s in scan_history if s[1] == username]
user_total_scans = len(user_scans)

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-label'>Total Scans</div>
            <div class='stat-number'>{user_total_scans}</div>
            <div style='color: rgba(255,255,255,0.5); font-size: 12px;'>All time</div>
        </div>
    """, unsafe_allow_html=True)

with stat_col2:
    high_risk_scans = len([s for s in user_scans if "High" in str(s[6])])
    st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-label'>High Risk Detected</div>
            <div class='stat-number' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); -webkit-background-clip: text;'>{high_risk_scans}</div>
            <div style='color: rgba(255,255,255,0.5); font-size: 12px;'>🔴 Requires attention</div>
        </div>
    """, unsafe_allow_html=True)

with stat_col3:
    st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-label'>Unread Alerts</div>
            <div class='stat-number' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); -webkit-background-clip: text;'>{unread_count}</div>
            <div style='color: rgba(255,255,255,0.5); font-size: 12px;'>New notifications</div>
        </div>
    """, unsafe_allow_html=True)

with stat_col4:
    if user_scans:
        latest_scan = user_scans[0]
        latest_risk = latest_scan[6] if len(latest_scan) > 6 else "N/A"
        risk_emoji = "🔴" if "High" in str(latest_risk) else ("🟠" if "Medium" in str(latest_risk) else "🟢")
    else:
        latest_risk = "N/A"
        risk_emoji = "📊"
    
    st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-label'>Last Scan Status</div>
            <div style='font-size: 24px; margin: 10px 0;'>{risk_emoji}</div>
            <div style='color: rgba(255,255,255,0.7); font-size: 14px; font-weight: 600;'>{latest_risk}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ------------------ TABS WITH ENHANCED STYLING ------------------
if unread_count > 0:
    tab_labels = ["Scan Device", f"Notifications ({unread_count})"]
else:
    tab_labels = ["Scan Device", "Notifications"]

tabs = st.tabs(tab_labels)

# ============================================
# TAB 1: SCAN DEVICE
# ============================================
with tabs[0]:
    st.markdown("### Network Security Scanner")
    st.write("Identify open ports and vulnerabilities in your IoT devices")
    
    scan_col1, scan_col2 = st.columns([3, 1])
    
    with scan_col1:
        target_ip = st.text_input(
            "Target IP Address", 
            "127.0.0.1",
            key="target_ip",
            help="Enter IPv4 address (e.g., 192.168.1.1)"
        )
    
    with scan_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        scan_button = st.button("Start Scan", key="start_scan", use_container_width=True)

    if scan_button:
        is_valid, error_msg = is_valid_ip(target_ip)
        
        if not is_valid:
            st.error(f"❌ {error_msg}")
            st.info("**Valid Examples:** 127.0.0.1, 192.168.1.1, 10.0.0.1")
        else:
            with st.spinner("Scanning in progress... Analyzing network security..."):
                try:
                    scan_results = scan_target(target_ip)

                    if scan_results:
                        df = pd.DataFrame(scan_results)
                        
                        st.success(f"✅ Scan completed successfully for {target_ip}")
                        
                        # AI Risk Prediction
                        overall_risk = predict_overall_risk(scan_results)
                        
                        # Color coding
                        if "High" in overall_risk:
                            risk_color = "#e74c3c"
                            risk_emoji = "🔴"
                            alert_class = "alert-high"
                        elif "Medium" in overall_risk:
                            risk_color = "#f39c12"
                            risk_emoji = "🟠"
                            alert_class = "alert-medium"
                        else:
                            risk_color = "#27ae60"
                            risk_emoji = "🟢"
                            alert_class = "alert-low"
                        
                        # Enhanced AI Prediction Display
                        st.markdown(f"""
                            <div class='alert-box {alert_class}' style='border-color: {risk_color};'>
                                <h2 style='margin: 0; color: {risk_color}; -webkit-text-fill-color: {risk_color};'>
                                    {risk_emoji} AI Risk Assessment: {overall_risk}
                                </h2>
                                <p style='margin: 10px 0 0 0; color: rgba(255,255,255,0.8);'>
                                    Based on {len(df)} detected ports and known vulnerability patterns
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Scan Results Table
                        st.markdown("### Detected Ports & Services")
                        
                        # Check for unknown ports
                        unknown_ports = [r for r in scan_results if r["Risk Level"] == "Unknown"]
                        if unknown_ports:
                            st.info(f"{len(unknown_ports)} port(s) not in database. Research links provided in recommendations.")
                        
                        st.dataframe(df, use_container_width=True, height=300)
                        
                        # Show research links for unknown ports
                        if unknown_ports:
                            with st.expander("Find out the Unknown Ports here!"):
                                st.write("The following ports were not found in our database. Click the links below to research them:")
                                for port_data in unknown_ports:
                                    port_num = port_data["Port"]
                                    service = port_data["Service"]
                                    research_url = get_port_info_url(port_num)
                                    st.markdown(f"- **Port {port_num}** ({service}): [Research this port →]({research_url})")

                        # Save to database
                        open_ports = len(df)
                        high_risks = df[df["Risk Level"].str.contains("High", case=False)]
                        risk_summary = f"High Risk: {len(high_risks)}, Total Ports: {open_ports}"
                        scan_id = save_scan_result(username, target_ip, open_ports, risk_summary, overall_risk)
                        
                        save_evidence(username, target_ip, scan_results, overall_risk)
                        
                        # Create notifications
                        high_risk_count = sum(1 for r in scan_results if "High" in r.get("Risk Level", ""))
                        medium_risk_count = sum(1 for r in scan_results if "Medium" in r.get("Risk Level", ""))
                        
                        if "High" in overall_risk:
                            create_notification(username, "⚠️ High Risk Device Detected!", 
                                f"Scan of {target_ip} revealed {high_risk_count} high-risk ports. Immediate action required.", 
                                "high_risk", scan_id)
                        elif "Medium" in overall_risk:
                            create_notification(username, "⚠️ Medium Risk Device Detected",
                                f"Scan of {target_ip} revealed {medium_risk_count} medium-risk ports. Review recommended.",
                                "medium_risk", scan_id)
                        else:
                            create_notification(username, "✅ Scan Complete - Device Secure",
                                f"Scan of {target_ip} completed. Device appears secure.",
                                "low_risk", scan_id)
                        
                        create_notification(username, f"Scan Complete: {target_ip}",
                            f"Detected {open_ports} ports. AI Assessment: {overall_risk}",
                            "scan_complete", scan_id)
                        
                        # ============================================
                        # CREATE TECHNICIAN ALERT (if High Risk)
                        # ============================================
                        if "High" in overall_risk:
                            # Import the function
                            from database import create_technician_alert
                            
                            # Collect high-risk port information
                            high_risk_items = [r for r in scan_results if "High" in r.get("Risk Level", "")]
                            
                            if high_risk_items:
                                # Format port numbers
                                port_numbers = ", ".join([str(item["Port"]) for item in high_risk_items])
                                
                                # Format port details
                                port_details_list = []
                                for item in high_risk_items:
                                    port_details_list.append(
                                        f"Port {item['Port']} ({item['Service']}): {item['Recommendation']}"
                                    )
                                port_details = " | ".join(port_details_list)
                                
                                # Create technician alert
                                create_technician_alert(
                                    username=username,
                                    target_ip=target_ip,
                                    risk_level="High Risk",
                                    high_risk_ports=port_numbers,
                                    port_details=port_details,
                                    scan_id=scan_id
                                )
                            
                            # Create "contact tech team" notification for user
                            create_notification(
                                username=username,
                                subject="Technical Team Notification",
                                message=(
                                    f"Security alert: Please schedule a meeting with the technical team "
                                    f"to address critical vulnerabilities.\n\n"
                                    f"Device: {target_ip}\n"
                                    f"Risk Level: High Risk\n"
                                    f"High-Risk Ports Detected: {high_risk_count}\n\n"
                                    f"The technical team has been notified and will be available to assist "
                                    f"with remediation steps."
                                ),
                                notification_type="tech_contact",
                                related_scan_id=scan_id
                            )
                        
                        st.success("Results saved | Evidence logged | Notifications generated")
                        
                        # Save session
                        st.session_state["last_scan_results"] = scan_results
                        st.session_state["last_target_ip"] = target_ip
                        st.session_state["last_overall_risk"] = overall_risk

                    else:
                        st.warning("No open ports detected on target device")

                except Exception as e:
                    st.error(f"❌ Scan failed: {e}")

    # Persisted results
    if "last_scan_results" in st.session_state:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### Previous Scan Results")

        scan_results = st.session_state["last_scan_results"]
        target_ip = st.session_state["last_target_ip"]
        overall_risk = st.session_state["last_overall_risk"]

        df = pd.DataFrame(scan_results)
        
        # Check for unknown ports in previous results
        unknown_ports_prev = [r for r in scan_results if r["Risk Level"] == "Unknown"]
        if unknown_ports_prev:
            st.info(f"{len(unknown_ports_prev)} port(s) not in database. Research links available below.")
        
        st.dataframe(df, use_container_width=True)
        
        # Show research links for unknown ports
        if unknown_ports_prev:
            with st.expander("Research Unknown Ports"):
                st.write("Click the links below to research unknown ports:")
                for port_data in unknown_ports_prev:
                    port_num = port_data["Port"]
                    service = port_data["Service"]
                    research_url = get_port_info_url(port_num)
                    st.markdown(f"- **Port {port_num}** ({service}): [Research this port →]({research_url})")

        # Download section
        st.markdown("### Export your results")
        
        csv_data = generate_csv(scan_results)
        pdf_data = generate_pdf(scan_results, target_ip, overall_risk)
        json_data = generate_json(scan_results, target_ip, overall_risk)

        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button("CSV Report", csv_data, f"scan_{target_ip}.csv", "text/csv")
        with col2:
            st.download_button("PDF Report", pdf_data, f"report_{target_ip}.pdf", "application/pdf")
        with col3:
            st.download_button("JSON Data", json_data, f"data_{target_ip}.json", "application/json")

# ============================================
# TAB 2: NOTIFICATIONS
# ============================================
with tabs[1]:
    st.markdown("### Security Alerts & Notifications")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        filter_option = st.radio(
            "Filter:",
            ["All", "Unread", "High Risk"],
            horizontal=True
        )
    
    with col2:
        if st.button("Mark All Read"):
            mark_all_as_read(username)
            st.success("All marked as read!")
            st.rerun()
    
    if filter_option == "Unread":
        notifications = get_user_notifications(username, unread_only=True)
    else:
        notifications = get_user_notifications(username, unread_only=False)
        if filter_option == "High Risk":
            notifications = [n for n in notifications if n[4] == "high_risk"]
    
    if notifications:
        st.info(f"{len(notifications)} notification(s)")
        
        for notif in notifications:
            notif_id, _, notif_subject, notif_message, notif_type, _, is_read, created_at, _ = notif
            
            if notif_type == "high_risk":
                icon, bg_color, border_color = "🔴", "rgba(231, 76, 60, 0.1)", "#e74c3c"
            elif notif_type == "medium_risk":
                icon, bg_color, border_color = "🟠", "rgba(243, 156, 18, 0.1)", "#f39c12"
            elif notif_type == "low_risk":
                icon, bg_color, border_color = "🟢", "rgba(39, 174, 96, 0.1)", "#27ae60"
            else:
                icon, bg_color, border_color = "📊", "rgba(52, 152, 219, 0.1)", "#3498db"
            
            read_badge = "🔴 NEW" if is_read == 0 else "✅ Read"
            
            st.markdown(f"""
                <div style='
                    background: {bg_color};
                    border-left: 5px solid {border_color};
                    padding: 20px;
                    border-radius: 10px;
                    margin: 15px 0;
                    backdrop-filter: blur(10px);
                '>
                    <h4 style='margin: 0; color: white; -webkit-text-fill-color: white;'>{icon} {notif_subject}</h4>
                    <p style='margin: 8px 0 0 0; font-size: 13px; color: rgba(255,255,255,0.6);'>
                        {created_at} | {read_badge}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("View Details"):
                st.write(notif_message)
                if is_read == 0:
                    if st.button(f"Mark as Read", key=f"read_{notif_id}"):
                        mark_notification_as_read(notif_id)
                        st.success("Marked as read!")
                        st.rerun()
    else:
        st.info("All caught up! No notifications to display.")

# ------------------ FOOTER ------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; padding: 20px; color: rgba(255,255,255,0.5);'>
        <p style='margin: 0; font-size: 13px;'>
            IoTGuard &copy; 2025 | Omni IoT Security Scanner
        </p>
        <p style='margin: 5px 0 0 0; font-size: 11px;'>
            Powered by AI | Protecting IoT Infrastructure Worldwide
        </p>
    </div>
""", unsafe_allow_html=True)