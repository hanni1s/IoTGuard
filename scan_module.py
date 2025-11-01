import nmap
from database import save_scan_result, create_notification, create_technician_alert
from ai_model import predict_overall_risk
from datetime import datetime

# =====================================================
# ENHANCED RISK RULES - 100+ PORTS COVERED!
# =====================================================
# Organized by category for better maintainability

RISK_RULES = {
    # ============ FILE TRANSFER & REMOTE ACCESS ============
    20: ("High", "FTP data transfer (unencrypted). Use SFTP instead."),
    21: ("High", "FTP uses cleartext credentials. Disable FTP or use SFTP."),
    22: ("Low", "SSH is secure if configured properly. Use strong keys and disable root login."),
    23: ("High", "Telnet is insecure. Disable Telnet, use SSH instead."),
    69: ("Medium", "TFTP has no authentication. Restrict access or disable."),
    115: ("Medium", "SFTP - Secure if properly configured with strong authentication."),
    989: ("Low", "FTPS data (secure FTP). Ensure certificates are valid."),
    990: ("Low", "FTPS control (secure FTP). Ensure certificates are valid."),
    
    # ============ EMAIL SERVICES ============
    25: ("Medium", "SMTP can be abused for spam. Enable authentication & TLS."),
    110: ("Medium", "POP3 uses cleartext. Use POP3S (995) or disable."),
    143: ("Medium", "IMAP uses cleartext. Use IMAPS (993) or disable."),
    465: ("Low", "SMTPS (secure SMTP). Ensure proper TLS configuration."),
    587: ("Medium", "SMTP submission port. Require authentication and TLS."),
    993: ("Low", "IMAPS (secure IMAP). Ensure certificates are valid."),
    995: ("Low", "POP3S (secure POP3). Ensure certificates are valid."),
    
    # ============ WEB SERVICES ============
    80: ("Medium", "HTTP is not encrypted. Redirect to HTTPS (443)."),
    443: ("Low", "HTTPS secure if configured properly. Keep certificates updated."),
    591: ("Medium", "FileMaker - Secure with authentication if needed."),
    8000: ("Medium", "HTTP alternate port. Often used by IoT devices - secure with authentication."),
    8008: ("Medium", "HTTP alternate. Common on routers/cameras - change default credentials."),
    8080: ("Medium", "HTTP proxy/alternate. Secure with authentication."),
    8081: ("Medium", "HTTP alternate. Often used for management interfaces."),
    8088: ("Medium", "HTTP alternate. Commonly used by IoT cameras."),
    8443: ("Medium", "HTTPS alternate. Used by IoT devices - ensure proper authentication."),
    8888: ("Medium", "HTTP alternate. Common on IP cameras - change default passwords."),
    9000: ("Medium", "Web services. Verify if service is required."),
    9090: ("Medium", "Web services alternate. Restrict access if unnecessary."),
    
    # ============ DATABASE SERVICES ============
    1433: ("High", "MS SQL Server. Should not be public-facing. Bind to localhost."),
    1434: ("High", "MS SQL Monitor. Vulnerable to attacks. Block externally."),
    3306: ("High", "MySQL should not be public. Bind to localhost only."),
    5432: ("Medium", "PostgreSQL. Should not be public. Use firewall rules."),
    5984: ("Medium", "CouchDB. Secure with authentication and firewall."),
    6379: ("High", "Redis cache. Extremely dangerous if exposed. Bind to localhost."),
    7000: ("Medium", "Cassandra. Should not be public. Use authentication."),
    7001: ("Medium", "Cassandra JMX. Restrict access with firewall."),
    9042: ("Medium", "Cassandra native. Secure with authentication."),
    9200: ("High", "Elasticsearch. Critical vulnerability if exposed. Use authentication."),
    9300: ("High", "Elasticsearch cluster. Should never be public."),
    27017: ("High", "MongoDB. Often targeted. Require authentication and bind to localhost."),
    27018: ("High", "MongoDB shard. Should not be exposed externally."),
    28017: ("High", "MongoDB web interface. Disable or restrict severely."),
    
    # ============ WINDOWS/SMB SERVICES ============
    135: ("High", "MS RPC common exploit target. Block externally with firewall."),
    137: ("High", "NetBIOS Name Service. Disable if not needed on network."),
    138: ("High", "NetBIOS Datagram. Disable if not required."),
    139: ("High", "NetBIOS Session Service insecure. Disable if not required."),
    445: ("High", "SMB vulnerable to exploits. Disable SMBv1, apply patches, use firewall."),
    
    # ============ REMOTE DESKTOP & VNC ============
    3389: ("High", "RDP brute-force target. Use VPN, restrict IPs, enable NLA and 2FA."),
    5800: ("High", "VNC web interface. Use strong passwords and encryption."),
    5900: ("High", "VNC remote desktop. Use SSH tunneling and strong authentication."),
    5901: ("High", "VNC display 1. Secure with VPN or SSH tunnel."),
    5902: ("High", "VNC display 2. Secure with VPN or SSH tunnel."),
    
    # ============ DNS & NETWORK SERVICES ============
    53: ("Medium", "DNS vulnerable if misconfigured. Restrict zone transfers and rate limit."),
    67: ("Low", "DHCP server. Normal for local networks, block externally."),
    68: ("Low", "DHCP client. Normal for local networks."),
    123: ("Low", "NTP time sync. Prevent amplification attacks with rate limiting."),
    161: ("High", "SNMP v1/v2 uses weak authentication. Use SNMPv3 with encryption."),
    162: ("High", "SNMP trap. Use SNMPv3 for security."),
    389: ("Medium", "LDAP directory. Use LDAPS (636) instead."),
    636: ("Low", "LDAPS (secure LDAP). Ensure certificates are valid."),
    5357: ("Medium", "WSDAPI used for Windows network discovery. Disable if not needed or restrict to trusted networks."),
    
    # ============ IoT & CAMERA SPECIFIC ============
    554: ("Medium", "RTSP streaming. Used by IP cameras - change default credentials."),
    1935: ("Medium", "RTMP streaming. Secure with authentication if required."),
    8000: ("Medium", "Common IoT management port. Change default passwords immediately."),
    8443: ("Medium", "IoT HTTPS. Often used by cameras - ensure strong authentication."),
    8843: ("Medium", "IoT camera HTTPS. Change default credentials."),
    9010: ("Medium", "Common on surveillance systems. Verify necessity and secure access."),
    37777: ("High", "Dahua DVR/NVR. Known vulnerabilities - update firmware and secure."),
    
    # ============ MESSAGING & COMMUNICATION ============
    1883: ("Medium", "MQTT (IoT messaging). Use authentication and TLS."),
    5222: ("Medium", "XMPP/Jabber. Use encryption and authentication."),
    5269: ("Medium", "XMPP server-to-server. Secure with TLS."),
    6667: ("Medium", "IRC. Legacy protocol, consider disabling."),
    8883: ("Low", "MQTT over TLS. Ensure certificates are valid."),
    
    # ============ VPN & TUNNELING ============
    500: ("Low", "IPSec IKE. Secure VPN protocol with proper configuration."),
    1194: ("Low", "OpenVPN. Secure if properly configured with certificates."),
    1701: ("Medium", "L2TP. Should be used with IPSec for security."),
    1723: ("Medium", "PPTP VPN. Outdated and vulnerable - use OpenVPN or WireGuard instead."),
    4500: ("Low", "IPSec NAT-T. Secure with proper configuration."),
    51820: ("Low", "WireGuard VPN. Modern and secure VPN protocol."),
    
    # ============ PROXY & SOCKS ============
    1080: ("High", "SOCKS proxy. Can be abused - require authentication."),
    3128: ("Medium", "HTTP proxy (Squid). Secure with authentication."),
    8118: ("Medium", "Privoxy. Secure proxy access with authentication."),
    9050: ("Medium", "Tor SOCKS proxy. Understand implications before exposing."),
    
    # ============ GAME SERVERS & MEDIA ============
    25565: ("Low", "Minecraft server. Use whitelist and authentication."),
    27015: ("Low", "Steam/Source games. Normal for game servers."),
    3478: ("Low", "STUN (VoIP/WebRTC). Normal for communication apps."),
    5060: ("Medium", "SIP (VoIP). Secure against scanning and attacks."),
    5061: ("Low", "SIP over TLS. Secure VoIP with encryption."),
    10000: ("Medium", "Webmin admin panel. Use HTTPS and strong passwords."),
    32400: ("Medium", "Plex media server. Secure with authentication."),
    
    # ============ DOCKER & CONTAINERS ============
    2375: ("High", "Docker API (unencrypted). NEVER expose publicly - use TLS."),
    2376: ("Medium", "Docker API (TLS). Secure with certificates and firewall."),
    2377: ("High", "Docker Swarm. Should never be public-facing."),
    6443: ("High", "Kubernetes API. Secure with strong authentication and RBAC."),
    8001: ("Medium", "Kubernetes dashboard. Use authentication and HTTPS."),
    10250: ("High", "Kubelet API. Should not be exposed - use firewall rules."),
    
    # ============ INDUSTRIAL IoT / SCADA ============
    102: ("High", "Siemens S7 PLC. Industrial control - isolate from internet."),
    502: ("High", "Modbus. Industrial protocol - should never be public."),
    1911: ("High", "Niagara Fox (BMS). Building management - isolate network."),
    2404: ("High", "IEC 60870-5-104. Industrial SCADA - air-gap recommended."),
    20000: ("High", "DNP3 (SCADA). Critical infrastructure - isolate completely."),
    44818: ("High", "EtherNet/IP. Industrial Ethernet - never expose publicly."),
    47808: ("High", "BACnet (building automation). Isolate from public networks."),
    
    # ============ PRINTER & DEVICE SERVICES ============
    515: ("Medium", "LPD printing. Legacy protocol - consider disabling."),
    631: ("Medium", "IPP (Internet Printing). Secure with authentication."),
    9100: ("Medium", "Raw printing. Common on network printers - secure network."),
    
    # ============ MISC SERVICES ============
    111: ("Medium", "RPC Portmapper. Can leak information - restrict access."),
    179: ("High", "BGP routing. Should only be on trusted networks."),
    514: ("Medium", "Syslog. Secure log transmission with encryption."),
    1900: ("Medium", "UPnP. Can be exploited - disable if not needed."),
    5353: ("Low", "mDNS (Bonjour). Normal for local discovery."),
    11211: ("High", "Memcached. Vulnerable to amplification attacks - bind to localhost."),
    50000: ("Medium", "SAP. Business software - secure with authentication."),
    62078: ("Medium", "Apple device sync (UPnP/iTunes) used by iPhones/iPads for file sharing. Restrict to trusted devices and local network only."),}


def get_port_info_url(port):
    """
    Generate a research URL for unknown ports.
    Returns a Speedguide.net link for port information.
    """
    return f"https://www.speedguide.net/port.php?port={port}"


def scan_target(target_ip):
    """Perform an Nmap scan and return structured results."""
    scanner = nmap.PortScanner()
    scanner.scan(target_ip, arguments="-sV")
    results = []

    for host in scanner.all_hosts():
        for proto in scanner[host].all_protocols():
            ports = scanner[host][proto].keys()
            for port in ports:
                service = scanner[host][proto][port]["name"]
                
                # Check if port is in our enhanced database
                if port in RISK_RULES:
                    risk, recommendation = RISK_RULES[port]
                else:
                    # Unknown port - provide research link
                    risk = "Unknown"
                    recommendation = f"Port not in database. Research recommended: {get_port_info_url(port)}"
                
                results.append({
                    "Port": port,
                    "Service": service,
                    "Risk Level": risk,
                    "Recommendation": recommendation
                })
    return results


def perform_scan_and_save(username, target_ip):
    """
    Perform scan, predict AI risk, save results to database,
    and automatically generate notifications.
    """
    print(f"[SCAN] Starting Nmap scan for {target_ip} by {username}...")
    scan_results = scan_target(target_ip)

    if not scan_results:
        print("[SCAN] No open ports detected.")
        return "No open ports detected."

    # AI Integration – Predict overall IoT risk using your model
    overall_risk = predict_overall_risk(scan_results)
    print(f"[AI] Predicted Overall Risk: {overall_risk}")

    # Prepare summary for database
    open_ports = len(scan_results)
    risk_summary = f"Detected {open_ports} open ports. AI Risk: {overall_risk}"
    print("[DB] Saving scan results...")

    # Save to database (username, IP, open_ports, summary, AI prediction)
    scan_id = save_scan_result(username, target_ip, open_ports, risk_summary, overall_risk)

    print("[DB] Scan results saved successfully.")
    
    # ============================================
    # AUTO-GENERATE NOTIFICATIONS
    # ============================================
    
    # Count high-risk ports
    high_risk_count = sum(1 for r in scan_results if "High" in r.get("Risk Level", ""))
    medium_risk_count = sum(1 for r in scan_results if "Medium" in r.get("Risk Level", ""))
    
    # Generate notification based on AI prediction
    if "High" in overall_risk:
        # High Risk Notification (URGENT)
        subject = "⚠️ High Risk Device Detected!"
        message = (
            f"Your scan of device {target_ip} has completed with a HIGH RISK assessment.\n\n"
            f"Scan Summary:\n"
            f"• Total Open Ports: {open_ports}\n"
            f"• High Risk Ports: {high_risk_count}\n"
            f"• Medium Risk Ports: {medium_risk_count}\n\n"
            f"⚠️ IMMEDIATE ACTION REQUIRED ⚠️\n"
            f"This device has critical vulnerabilities that should be addressed immediately. "
            f"Please review the full scan report and implement recommended security measures.\n\n"
            f"Scanned at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        create_notification(
            username=username,
            subject=subject,
            message=message,
            notification_type="high_risk",
            related_scan_id=scan_id
        )
        print(f"[NOTIFICATION] Created HIGH RISK alert for {username}")
    
        # ============================================
        # CREATE TECHNICIAN ALERT
        # ============================================
        
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
            print(f"[TECH ALERT] Created technician alert for {username}'s scan")
        
        # ============================================
        # NOTIFY USER TO CONTACT TECH TEAM
        # ============================================
        
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
        print(f"[NOTIFICATION] Created tech contact notification for {username}")
        
    elif "Medium" in overall_risk:
        # Medium Risk Notification (MODERATE)
        subject = "⚠️ Medium Risk Device Detected"
        message = (
            f"Your scan of device {target_ip} has completed with a MEDIUM RISK assessment.\n\n"
            f"Scan Summary:\n"
            f"• Total Open Ports: {open_ports}\n"
            f"• High Risk Ports: {high_risk_count}\n"
            f"• Medium Risk Ports: {medium_risk_count}\n\n"
            f"Review Recommended\n"
            f"This device has some vulnerabilities that should be reviewed. "
            f"Please check the scan report and consider implementing the recommended security improvements.\n\n"
            f"Scanned at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        create_notification(
            username=username,
            subject=subject,
            message=message,
            notification_type="medium_risk",
            related_scan_id=scan_id
        )
        print(f"[NOTIFICATION] Created MEDIUM RISK alert for {username}")
        
    else:
        # Low Risk Notification (ALL CLEAR)
        subject = "Scan Complete - Device Secure"
        message = (
            f"Your scan of device {target_ip} has completed with a LOW RISK assessment.\n\n"
            f"Scan Summary:\n"
            f"• Total Open Ports: {open_ports}\n"
            f"• High Risk Ports: {high_risk_count}\n"
            f"• Medium Risk Ports: {medium_risk_count}\n\n"
            f"Good News!\n"
            f"This device appears to be properly secured. Continue following security best practices "
            f"and perform regular scans to maintain security.\n\n"
            f"Scanned at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        create_notification(
            username=username,
            subject=subject,
            message=message,
            notification_type="low_risk",
            related_scan_id=scan_id
        )
        print(f"[NOTIFICATION] Created LOW RISK notification for {username}")
    
    # Always create a general "scan complete" notification too
    create_notification(
        username=username,
        subject=f"Scan Complete: {target_ip}",
        message=(
            f"Your IoT security scan has completed successfully.\n\n"
            f"Target: {target_ip}\n"
            f"Ports Detected: {open_ports}\n"
            f"AI Assessment: {overall_risk}\n\n"
            f"View your dashboard to see the detailed results."
        ),
        notification_type="scan_complete",
        related_scan_id=scan_id
    )
    print(f"[NOTIFICATION] Created SCAN COMPLETE notification for {username}")

    return overall_risk