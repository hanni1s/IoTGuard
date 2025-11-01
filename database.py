import sqlite3
from pathlib import Path
from datetime import datetime

# ----------------------------
# DATABASE PATH SETUP
# ----------------------------
DB_PATH = Path("iotguard.db")

def init_db():
    """Initialize database and create tables if not exist."""
    # Ensure the directory exists (safety measure)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # --- Users Table ---
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # --- Scan History Table ---
    c.execute('''
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            target_ip TEXT,
            open_ports TEXT,
            risk_summary TEXT,
            date TEXT,
            ai_prediction TEXT DEFAULT 'N/A'
        )
    ''')

    # --- Notifications Table  ---
    c.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            subject TEXT,
            message TEXT,
            notification_type TEXT,
            related_scan_id INTEGER,
            is_read INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            read_at TEXT
        )
    ''')

    # --- Technician Alerts Table ---
    c.execute('''
        CREATE TABLE IF NOT EXISTS technician_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            target_ip TEXT,
            risk_level TEXT,
            high_risk_ports TEXT,
            port_details TEXT,
            alert_message TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            is_read INTEGER DEFAULT 0,
            scan_id INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()


def save_scan_result(username, target_ip, open_ports, risk_summary, ai_prediction="N/A"):
    """Save a new scan record into the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Convert open_ports to string if it's a list (e.g., [22, 80, 443])
    if isinstance(open_ports, list):
        open_ports = ",".join(map(str, open_ports))

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute('''
        INSERT INTO scan_history (username, target_ip, open_ports, risk_summary, date, ai_prediction)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, target_ip, open_ports, risk_summary, date_str, ai_prediction))
    
    scan_id = c.lastrowid  # Get the ID of the scan we just inserted
    
    conn.commit()
    conn.close()
    
    return scan_id  # Return scan_id so we can link notifications to it


def get_scan_history():
    """Retrieve all scan records from the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM scan_history ORDER BY date DESC")
    data = c.fetchall()
    conn.close()
    return data


def get_user_list():
    """Retrieve all registered users (for technician/admin view)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, role, created_at FROM users ORDER BY id ASC")
    users = c.fetchall()
    conn.close()
    return users


# ============================================
# NOTIFICATION FUNCTIONS 
# ============================================

def create_notification(username, subject, message, notification_type, related_scan_id=None):
    """
    Create a new notification for a user.
    
    Args:
        username: Who receives the notification
        subject: Notification title/subject
        message: Notification body/content
        notification_type: Type of notification (high_risk, medium_risk, low_risk, scan_complete, etc.)
        related_scan_id: ID of the scan this notification is about (optional)
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute('''
        INSERT INTO notifications (username, subject, message, notification_type, related_scan_id, is_read, created_at)
        VALUES (?, ?, ?, ?, ?, 0, ?)
    ''', (username, subject, message, notification_type, related_scan_id, created_at))
    
    conn.commit()
    conn.close()
    
    print(f"[NOTIFICATION] Created '{notification_type}' notification for {username}")


def get_user_notifications(username, unread_only=False):
    """
    Get all notifications for a specific user.
    
    Args:
        username: Username to get notifications for
        unread_only: If True, only return unread notifications
    
    Returns:
        List of notifications (tuples)
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if unread_only:
        c.execute('''
            SELECT id, username, subject, message, notification_type, related_scan_id, is_read, created_at, read_at
            FROM notifications
            WHERE username = ? AND is_read = 0
            ORDER BY created_at DESC
        ''', (username,))
    else:
        c.execute('''
            SELECT id, username, subject, message, notification_type, related_scan_id, is_read, created_at, read_at
            FROM notifications
            WHERE username = ?
            ORDER BY created_at DESC
        ''', (username,))
    
    notifications = c.fetchall()
    conn.close()
    return notifications


def get_unread_count(username):
    """Get the count of unread notifications for a user."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        SELECT COUNT(*) FROM notifications
        WHERE username = ? AND is_read = 0
    ''', (username,))
    
    count = c.fetchone()[0]
    conn.close()
    return count


def mark_notification_as_read(notification_id):
    """Mark a notification as read."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    read_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute('''
        UPDATE notifications
        SET is_read = 1, read_at = ?
        WHERE id = ?
    ''', (read_at, notification_id))
    
    conn.commit()
    conn.close()
    
    print(f"[NOTIFICATION] Marked notification {notification_id} as read")


def mark_all_as_read(username):
    """Mark all notifications as read for a specific user."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    read_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute('''
        UPDATE notifications
        SET is_read = 1, read_at = ?
        WHERE username = ? AND is_read = 0
    ''', (read_at, username))
    
    conn.commit()
    conn.close()
    
    print(f"[NOTIFICATION] Marked all notifications as read for {username}")


def delete_notification(notification_id):
    """Delete a specific notification."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('DELETE FROM notifications WHERE id = ?', (notification_id,))
    
    conn.commit()
    conn.close()
    
    print(f"[NOTIFICATION] Deleted notification {notification_id}")

# ============================================
# TECHNICIAN ALERT FUNCTIONS 
# ============================================

def create_technician_alert(username, target_ip, risk_level, high_risk_ports, port_details, scan_id):
    """
    Create a new alert for technicians when high-risk devices are detected.
    
    Args:
        username: User who performed the scan
        target_ip: IP address of the vulnerable device
        risk_level: Risk level (High/Medium/Low)
        high_risk_ports: Comma-separated list of high-risk port numbers
        port_details: Description of the vulnerabilities
        scan_id: ID of the related scan
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    alert_message = f"User {username} detected {risk_level} device at {target_ip}"
    
    c.execute('''
        INSERT INTO technician_alerts (username, target_ip, risk_level, high_risk_ports, port_details, alert_message, created_at, is_read, scan_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?)
    ''', (username, target_ip, risk_level, high_risk_ports, port_details, alert_message, created_at, scan_id))
    
    conn.commit()
    conn.close()
    
    print(f"[TECH ALERT] Created alert for scan {scan_id} by {username}")


def get_technician_alerts(unread_only=False):
    """
    Get all technician alerts.
    
    Args:
        unread_only: If True, only return unread alerts
    
    Returns:
        List of alerts (tuples)
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if unread_only:
        c.execute('''
            SELECT id, username, target_ip, risk_level, high_risk_ports, port_details, alert_message, created_at, is_read, scan_id
            FROM technician_alerts
            WHERE is_read = 0
            ORDER BY created_at DESC
        ''')
    else:
        c.execute('''
            SELECT id, username, target_ip, risk_level, high_risk_ports, port_details, alert_message, created_at, is_read, scan_id
            FROM technician_alerts
            ORDER BY created_at DESC
        ''')
    
    alerts = c.fetchall()
    conn.close()
    return alerts


def get_unread_alert_count():
    """Get the count of unread technician alerts."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM technician_alerts WHERE is_read = 0')
    count = c.fetchone()[0]
    
    conn.close()
    return count


def mark_alert_as_read(alert_id):
    """Mark a technician alert as read."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('UPDATE technician_alerts SET is_read = 1 WHERE id = ?', (alert_id,))
    
    conn.commit()
    conn.close()
    
    print(f"[TECH ALERT] Marked alert {alert_id} as read")


def mark_all_alerts_as_read():
    """Mark all technician alerts as read."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('UPDATE technician_alerts SET is_read = 1 WHERE is_read = 0')
    
    conn.commit()
    conn.close()
    
    print(f"[TECH ALERT] Marked all alerts as read")