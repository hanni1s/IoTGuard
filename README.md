#  IoTGuard - Omni IoT Security Scanner


**AI-Powered IoT Vulnerability Scanner | Advanced Threat Detection**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Tech Stack](#-tech-stack)

</div>

---

## Table of Contents

- [About](#-about)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [System Architecture](#-system-architecture)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## About

**IoTGuard** is a comprehensive IoT security scanner that helps identify vulnerabilities in Internet of Things (IoT) devices through intelligent network scanning and AI-powered risk assessment. Built with enterprise-grade security practices, IoTGuard provides real-time threat detection, automated escalation workflows, and professional reporting capabilities.

### Why IoTGuard?

- **Comprehensive Scanning**: Detects open ports and services on IoT devices
- **AI-Powered Analysis**: Machine learning risk prediction with 100+ port definitions
- **Automatic Escalation**: Technician alert system for high-risk findings
- **Professional Reports**: Export findings in PDF, CSV, and JSON formats
- **Enterprise Security**: Bcrypt encryption, role-based access control
- **Beautiful UI**: Modern, animated interface with real-time updates

---

## Features

### Security & Authentication
- **Secure Login System** with bcrypt password hashing
- **Role-Based Access Control** (Users & Technicians)
- **Fixed Technician Accounts** to prevent privilege escalation
- **Session Management** with secure logout

### Network Scanning
- **Nmap Integration** for comprehensive port scanning
- **100+ Port Database** covering IoT devices, industrial systems, and common services
- **Service Detection** with version identification
- **IP Validation** to prevent invalid scans

### AI Risk Intelligence
- **Machine Learning Model** using Decision Tree Classification
- **Real-Time Risk Prediction** (High/Medium/Low)
- **Predictive Analytics** for trend forecasting
- **Historical Data Analysis** with visual insights

### Alert & Notification System
- **User Notifications** for scan completion and risk findings
- **Technician Alert System** with automatic escalation for high-risk devices
- **Detailed Port Information** including vulnerability descriptions
- **Read/Unread Status Tracking**
- **Email Architecture** ready for production deployment

### Reporting & Analytics
- **PDF Reports** with professional formatting and branding
- **CSV Export** for data analysis
- **JSON Export** with complete metadata
- **Evidence Logging** for audit trails
- **Interactive Dashboards** with Plotly visualizations

### User Experience
- **Beautiful Animated UI** with particle effects
- **Responsive Design** optimized for all screen sizes
- **Real-Time Updates** with progress indicators
- **Intuitive Navigation** with tabbed interfaces
- **Dark Theme** with gradient accents

---

## Tech Stack

### Backend
- **Python 3.8+** - Core programming language
- **Nmap** - Network scanning engine
- **SQLite3** - Database management
- **Scikit-learn** - Machine learning framework
- **Pandas & NumPy** - Data processing

### Frontend
- **Streamlit** - Web application framework
- **Plotly** - Interactive visualizations
- **CSS3** - Custom styling and animations

### Security
- **Bcrypt** - Password hashing
- **SSL/TLS** - Secure communications (production)

### Reporting
- **ReportLab** - PDF generation
- **Pandas** - CSV/Excel export
- **JSON** - Structured data export

---

## Installation

### Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **Nmap** (Required for scanning)
   - **Windows**: Download from [nmap.org](https://nmap.org/download.html)
   - **Linux**: 
     ```bash
     sudo apt-get update
     sudo apt-get install nmap
     ```
   - **macOS**: 
     ```bash
     brew install nmap
     ```

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/hanni1s/IoTGuard
   cd IoTGuard
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   
   # Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   streamlit --version
   nmap --version
   ```

---

## Usage

### Starting the Application

1. **Run the main application**
   ```bash
   streamlit run main.py
   ```

2. **Access the application**
   - Open your browser and navigate to `http://localhost:8501`

### First Time Setup

1. **Create a User Account**
   - Click on "Register" tab
   - Enter username and strong password
   - Users are automatically registered (technician accounts are pre-provisioned)

2. **Create Technician Account** (One-time setup)
   - Temporarily enable technician registration in `main.py`
   - Register one technician account
   - Re-lock registration to User-only

### Using IoTGuard

#### As a User:
1. **Login** with your credentials
2. **Navigate** to "Scan Device" tab
3. **Enter target IP** address (e.g., 192.168.1.1)
4. **Click "Start Scan"** and wait for results
5. **View AI Risk Assessment** and detected ports
6. **Export Reports** in PDF/CSV/JSON format
7. **Check Notifications** for alerts and recommendations

#### As a Technician:
1. **Login** with technician credentials
2. **View Overview** dashboard for system-wide analytics
3. **Monitor Alerts** in the Security Alerts tab
4. **Analyze Trends** in AI Intelligence section
5. **Review Scan Records** with advanced filtering
6. **Download Reports** for compliance and auditing

---

## Project Structure

```
IOTGUARD_NEW/
├── main.py                      # Entry point (Login page)
├── pages/
│   ├── user_dashboard.py        # User interface
│   └── technician_dashboard.py  # Technician interface
├── ai_model.py                  # AI risk prediction model
├── database.py                  # Database operations
├── scan_module.py               # Network scanning logic
├── report_module.py             # Report generation (PDF/CSV/JSON)
├── evidence_collect.py          # Evidence logging
├── view_db.py                   # Database viewer utility
├── logo_latest.png              # Application branding
├── iotguard.db                  # SQLite database
├── ai_risk_model.pkl            # Trained AI model
├── evidence_logs/               # Scan evidence storage
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## System Architecture

### Database Schema

#### Users Table
```sql
- id: INTEGER PRIMARY KEY
- username: TEXT UNIQUE
- password: TEXT (bcrypt hashed)
- role: TEXT (User/Technician)
- created_at: TEXT
```

#### Scan History Table
```sql
- id: INTEGER PRIMARY KEY
- username: TEXT
- target_ip: TEXT
- open_ports: TEXT
- risk_summary: TEXT
- date: TEXT
- ai_prediction: TEXT
```

#### Notifications Table
```sql
- id: INTEGER PRIMARY KEY
- username: TEXT
- subject: TEXT
- message: TEXT
- notification_type: TEXT
- related_scan_id: INTEGER
- is_read: INTEGER
- created_at: TEXT
- read_at: TEXT
```

#### Technician Alerts Table
```sql
- id: INTEGER PRIMARY KEY
- username: TEXT
- target_ip: TEXT
- risk_level: TEXT
- high_risk_ports: TEXT
- port_details: TEXT
- alert_message: TEXT
- created_at: TEXT
- is_read: INTEGER
- scan_id: INTEGER
```

### Workflow Diagram

```
User Scan → Nmap Analysis → AI Risk Prediction
                                    ↓
                          Database Storage
                                    ↓
                    ┌───────────────┴───────────────┐
                    ↓                               ↓
            User Notification              Technician Alert
          (with recommendations)        (with port details)
```

---

## Security Best Practices

IoTGuard implements several security measures:

1. **Password Security**
   - Bcrypt hashing (cost factor 12)
   - Minimum 8 characters with complexity requirements
   - Secure password change functionality

2. **Access Control**
   - Role-based permissions
   - Session management
   - Technician account provisioning (prevents self-escalation)

3. **Data Protection**
   - SQL injection prevention through parameterized queries
   - Input validation for IP addresses
   - Secure evidence logging

4. **Audit Trail**
   - Complete scan history
   - Notification tracking
   - Evidence preservation

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/iotguard.git

# Create development branch
git checkout -b dev

# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Nmap** - Network scanning engine
- **Streamlit** - Web application framework
- **Scikit-learn** - Machine learning library
- **Speedguide.net** - Port information database
- Special thanks to all contributors and testers

---

## Contact

**Project Maintainer**: Hanis Masturina

- GitHub: [@hanni1s](https://github.com/hanni1s)
- Email: hanismstrn@gmail.com

---

## Academic Information

This project was developed as part of Politeknik Ungku Omar - Diploma in DIgital Technology (Information Security)
Team members: Hanis Masturina, Sofea, Nur Naida Hanim

---

## 🚀 Future Enhancements

Planned features for future releases:

- [ ] Real SMTP email integration
- [ ] Multi-language support
- [ ] Docker containerization
- [ ] REST API for integration
- [ ] Mobile application
- [ ] CVE database integration
- [ ] Scheduled automated scans
- [ ] Custom port rule definitions
- [ ] Export to SIEM platforms
- [ ] Network topology mapping

---

## ⚠️ Disclaimer

IoTGuard is intended for authorized security testing and educational purposes only. Users are responsible for ensuring they have proper authorization before scanning any network or device. Unauthorized access to computer systems is illegal.

---

