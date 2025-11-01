import streamlit as st
import sqlite3
from pathlib import Path
from database import init_db
import re
import bcrypt

# ----------------------------
# INITIALIZE DATABASE
# ----------------------------
init_db()

# ----------------------------
# PAGE CONFIGURATION
# ----------------------------
st.set_page_config(
    page_title="IoTGuard - Login", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ----------------------------
# MEGA ENHANCED STYLING WITH ANIMATIONS
# ----------------------------
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Animated Background */
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: white;
        position: relative;
        overflow: hidden;
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
    
    /* Wave Animation at Bottom */
    .wave {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 200px;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 320'%3E%3Cpath fill='%23667eea' fill-opacity='0.1' d='M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,112C672,96,768,96,864,112C960,128,1056,160,1152,165.3C1248,171,1344,149,1392,138.7L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z'%3E%3C/path%3E%3C/svg%3E");
        background-size: cover;
        animation: wave 10s linear infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes wave {
        0% {
            background-position: 0 0;
        }
        100% {
            background-position: 1440px 0;
        }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Container positioning */
    .block-container {
        position: relative;
        z-index: 1;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    
    /* Hero Logo - BIGGER! */
    .hero-logo {
        text-align: center;
        margin-bottom: 50px;
        margin-top: 30px;
        animation: logoFloat 3s ease-in-out infinite;
    }
    
    .logo-image {
        max-width: 450px;  /* Made BIGGER! */
        width: 90%;
        height: auto;
        filter: drop-shadow(0 0 50px rgba(102, 126, 234, 0.9));
        animation: logoFloat 3s ease-in-out infinite, logoGlow 3s ease-in-out infinite;
    }
    
    @keyframes logoFloat {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-20px);
        }
    }
    
    @keyframes logoGlow {
        0%, 100% {
            filter: drop-shadow(0 0 50px rgba(102, 126, 234, 0.7));
        }
        50% {
            filter: drop-shadow(0 0 90px rgba(102, 126, 234, 1));
        }
    }
    
    /* REMOVED - App Logo Text Styling */
    /* No longer needed since we're using only the logo image */
    
    /* Login Card Container */
    .login-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        padding: 50px 40px;
        box-shadow: 0 25px 80px rgba(0, 0, 0, 0.4);
        animation: slideUp 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .login-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.03), transparent);
        animation: shimmer 3s linear infinite;
    }
    
    @keyframes shimmer {
        0% {
            transform: translateX(-100%) translateY(-100%) rotate(45deg);
        }
        100% {
            transform: translateX(100%) translateY(100%) rotate(45deg);
        }
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Input Field Styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 15px !important;
        padding: 18px !important;
        font-size: 16px !important;
        transition: all 0.4s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border: 2px solid #667eea !important;
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.5) !important;
        background: rgba(255, 255, 255, 0.1) !important;
        transform: translateY(-2px);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }
    
    /* Select Box Styling */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:hover {
        border: 2px solid rgba(102, 126, 234, 0.5) !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 18px 50px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        width: 100% !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5) !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 45px rgba(102, 126, 234, 0.7) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-2px) !important;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 10px;
        margin-bottom: 40px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: rgba(255, 255, 255, 0.6);
        border-radius: 15px;
        padding: 15px 30px;
        font-weight: 600;
        font-size: 15px;
        border: none;
        transition: all 0.4s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.05);
        color: rgba(255, 255, 255, 0.9);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        transform: translateY(-2px);
    }
    
    /* Feature Box Styling */
    .feature-box {
        text-align: center;
        padding: 25px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        margin: 10px 0;
        transition: all 0.4s ease;
        cursor: pointer;
    }
    
    .feature-box:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(102, 126, 234, 0.5);
    }
    
    .feature-icon {
        font-size: 48px;
        margin-bottom: 15px;
        animation: bounce 2s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    .feature-text {
        color: rgba(255, 255, 255, 0.9);
        font-size: 15px;
        font-weight: 600;
    }
    
    /* Alert Styling */
    .stSuccess, .stWarning, .stError, .stInfo {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        border-left: 4px solid !important;
        padding: 18px !important;
        animation: slideInRight 0.5s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .stSuccess {
        border-left-color: #27ae60 !important;
        background: rgba(39, 174, 96, 0.1) !important;
    }
    
    .stWarning {
        border-left-color: #f39c12 !important;
        background: rgba(243, 156, 18, 0.1) !important;
    }
    
    .stError {
        border-left-color: #e74c3c !important;
        background: rgba(231, 76, 60, 0.1) !important;
    }
    
    /* Label Styling */
    label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        margin-bottom: 10px !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent);
        margin: 40px 0;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    </style>
    
    <!-- Particle Effect -->
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
        <div class="particle" style="width: 3px; height: 3px; left: 18%; animation-duration: 25s; animation-delay: 10s;"></div>
        <div class="particle" style="width: 6px; height: 6px; left: 48%; animation-duration: 19s; animation-delay: 3s;"></div>
        <div class="particle" style="width: 4px; height: 4px; left: 68%; animation-duration: 22s; animation-delay: 6s;"></div>
        <div class="particle" style="width: 5px; height: 5px; left: 88%; animation-duration: 18s; animation-delay: 2s;"></div>

    </div>
    
    <!-- Wave Effect -->
    <div class="wave"></div>
""", unsafe_allow_html=True)

# ----------------------------
# DATABASE PATH
# ----------------------------
DB_PATH = Path("iotguard.db")

# ----------------------------
# HELPER FUNCTIONS
# ----------------------------
def is_strong_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    if not re.search(r"[@$!%*?&#]", password):
        return False, "Password must contain at least one special character."
    return True, ""

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def add_user(username, password, role):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        hashed_pw = hash_password(password)
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                  (username, hashed_pw, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password, role):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=? AND role=?", (username, role))
    result = c.fetchone()
    conn.close()
    if result:
        return verify_password(password, result[0])
    return False

def update_password(username, old_pw, new_pw):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    user = c.fetchone()
    if not user:
        conn.close()
        return False, "User not found."
    if not verify_password(old_pw, user[0]):
        conn.close()
        return False, "Current password is incorrect."
    valid, message = is_strong_password(new_pw)
    if not valid:
        conn.close()
        return False, message
    hashed_new_pw = hash_password(new_pw)
    c.execute("UPDATE users SET password=? WHERE username=?", (hashed_new_pw, username))
    conn.commit()
    conn.close()
    return True, "Password updated successfully."

# ----------------------------
# IOTGUARD LOGO
# ----------------------------
from pathlib import Path
import base64

# Load and encode logo
logo_path = Path("logo_latest.png")
if logo_path.exists():
    with open(logo_path, "rb") as f:
        logo_data = base64.b64encode(f.read()).decode()
    
    st.markdown(f"""
        <div class='hero-logo'>
            <img src='data:image/png;base64,{logo_data}' class='logo-image' alt='IoTGuard Logo'>
        </div>
    """, unsafe_allow_html=True)
else:
    # Fallback to shield if logo not found
    st.markdown("""
        <div class='hero-logo'>
            <div style='font-size: 120px;'>🛡️</div>
        </div>
    """, unsafe_allow_html=True)

# REMOVED: Text title and subtitle (using logo only now!)

# ----------------------------
# FEATURE HIGHLIGHTS
# ----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class='feature-box'>
            <div class='feature-icon'>🔍</div>
            <div class='feature-text'>Network Scanning</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='feature-box'>
            <div class='feature-icon'>🤖</div>
            <div class='feature-text'>AI Analysis</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class='feature-box'>
            <div class='feature-icon'>📊</div>
            <div class='feature-text'>Real-time Reports</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------
# TABS
# ----------------------------
tabs = st.tabs(["Login", "Register", "Change Password"])

# ----------------------------
# LOGIN TAB
# ----------------------------
with tabs[0]:
    st.markdown("### Welcome Back!")
    st.write("Sign in to access your security dashboard")
    
    username = st.text_input("Username", key="login_user", placeholder="Enter your username")
    password = st.text_input("Password", type="password", key="login_pass", placeholder="Enter your password")
    role = st.selectbox("Select Role", ["User", "Technician"], key="login_role")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Login Now", key="login_btn"):
        if not username or not password:
            st.warning("⚠️ Please fill in both username and password.")
        else:
            with st.spinner("Authenticating..."):
                if verify_user(username, password, role):
                    st.success(f"Hey! Welcome back, {username}!")
                    st.session_state["logged_in"] = True
                    st.session_state["role"] = role
                    st.session_state["username"] = username
                    if role == "User":
                        st.switch_page("pages/user_dashboard.py")
                    else:
                        st.switch_page("pages/technician_dashboard.py")
                else:
                    st.error("❌ Invalid credentials. Please try again.")

# ----------------------------
# REGISTER TAB
# ----------------------------
with tabs[1]:
    st.markdown("### Create Your Account")
    st.write("Join IoTGuard and scan your devices now!")
    
    new_username = st.text_input("Username", key="reg_user", placeholder="Choose a username")
    new_password = st.text_input("Password", type="password", key="reg_pass", placeholder="Create strong password")
    new_role = "User"
    st.info("New accounts are created as Users. Technician access is managed by administrators.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Create Account", key="reg_btn"):
        if not new_username or not new_password:
            st.warning("⚠️ Please fill in all fields.")
        else:
            valid, message = is_strong_password(new_password)
            if not valid:
                st.warning(f"⚠️ {message}")
            else:
                if add_user(new_username, new_password, new_role):
                    st.success("Yeay, Account created! You can now log in.")
                else:
                    st.warning("⚠️ Username already exists.")

# ----------------------------
# CHANGE PASSWORD TAB
# ----------------------------
with tabs[2]:
    st.markdown("### Update Password")
    st.write("Keep your account secure")
    
    username_cp = st.text_input("Username", key="cp_user", placeholder="Your username")
    old_pw = st.text_input("Current Password", type="password", key="cp_old", placeholder="Current password")
    new_pw = st.text_input("New Password", type="password", key="cp_new", placeholder="New password")
    confirm_pw = st.text_input("Confirm Password", type="password", key="cp_confirm", placeholder="Confirm new password")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Update Password", key="cp_btn"):
        if not all([username_cp, old_pw, new_pw, confirm_pw]):
            st.warning("⚠️ Please fill in all fields.")
        elif new_pw != confirm_pw:
            st.warning("⚠️ Passwords don't match.")
        else:
            with st.spinner("Updating..."):
                success, message = update_password(username_cp, old_pw, new_pw)
                if success:
                    st.success(f"✅ {message}")
                else:
                    st.warning(f"⚠️ {message}")

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; padding: 30px; color: rgba(255,255,255,0.5);'>
        <p style='margin: 0; font-size: 14px; font-weight: 600;'>
            IoTGuard &copy; 2025
        </p>
        <p style='margin: 10px 0 0 0; font-size: 12px;'>
            Protecting IoT Infrastructure Worldwide | Powered by AI
        </p>
    </div>
""", unsafe_allow_html=True)