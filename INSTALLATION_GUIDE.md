# IoTGuard - Installation Guide for Beginners

**Welcome!** This guide will help you set up and run IoTGuard on your computer, even if you've never used Python before! 😊

---

## 📋 Table of Contents
1. [What You Need to Download](#-what-you-need-to-download)
2. [Windows Installation](#-windows-installation)
3. [Linux Installation](#-linux-installation)
4. [Running IoTGuard](#-running-iotguard)
5. [Troubleshooting](#-troubleshooting)

---

## What You Need to Download

Before running IoTGuard, you need to install:

1. **Python** (3.8 or higher) - The programming language
2. **Nmap** - Network scanning tool
3. **IoTGuard** - This project!

**Don't worry!** I'll guide you through each step! 💪

---

## Windows Installation

### Step 1: Install Python

1. **Download Python:**
   - Go to [python.org/downloads](https://www.python.org/downloads/)
   - Click the big yellow button **"Download Python 3.x.x"**
   - Save the file

2. **Install Python:**
   - Run the downloaded file
   - ⚠️ **IMPORTANT:** Check ✅ **"Add Python to PATH"** (at the bottom!)
   - Click **"Install Now"**
   - Wait for installation to complete
   - Click **"Close"**

3. **Verify Installation:**
   - Press `Windows Key + R`
   - Type `cmd` and press Enter
   - In the black window, type:
     ```bash
     python --version
     ```
   - You should see: `Python 3.x.x`

### Step 2: Install Nmap

1. **Download Nmap:**
   - Go to [nmap.org/download.html](https://nmap.org/download.html)
   - Click **"nmap-x.xx-setup.exe"** (Latest stable release)
   - Save the file

2. **Install Nmap:**
   - Run the downloaded file
   - Click **"Next"** through all screens
   - Keep all default options
   - Click **"Install"**
   - Click **"Finish"**

3. **Verify Installation:**
   - Open Command Prompt (cmd)
   - Type:
     ```bash
     nmap --version
     ```
   - You should see: `Nmap version x.xx`

### Step 3: Download IoTGuard

1. **Download from GitHub:**
   - Go to [https://github.com/hanni1s/IoTGuard](https://github.com/hanni1s/IoTGuard)
   - Click the green **"Code"** button
   - Click **"Download ZIP"**
   - Save the file

2. **Extract the ZIP:**
   - Right-click on the downloaded ZIP file
   - Click **"Extract All..."**
   - Choose where to extract (e.g., Desktop)
   - Click **"Extract"**

3. **Open the Folder:**
   - Open the extracted folder
   - You should see files like `main.py`, `requirements.txt`, etc.

### Step 4: Install IoTGuard Dependencies

1. **Open Command Prompt in the IoTGuard folder:**
   - In the IoTGuard folder, hold **Shift** and **Right-click** on empty space
   - Click **"Open PowerShell window here"** (or "Open command window here")

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```
   - Wait for all packages to install (this may take 2-5 minutes)
   - You'll see lots of text scrolling - that's normal!

3. **Wait for completion:**
   - When you see a message like "Successfully installed..." you're done!

### Step 5: Run IoTGuard! 🎉

1. **Start the application:**
   ```bash
   streamlit run main.py
   ```

2. **Wait for browser to open:**
   - A browser window will automatically open
   - You'll see IoTGuard's beautiful login page! ✨

3. **Create an account:**
   - Click **"Register"** tab
   - Create your username and password
   - Click **"Create Account"**
   - Now you can login and start scanning! 🔍

---

## Linux Installation

### Step 1: Install Python and Pip

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip
```

### Step 2: Install Nmap

**Ubuntu/Debian:**
```bash
sudo apt install nmap
```

**Fedora:**
```bash
sudo dnf install nmap
```

**Arch Linux:**
```bash
sudo pacman -S nmap
```

### Step 3: Download and Setup IoTGuard

1. **Clone or download from GitHub:**
   ```bash
   cd ~
   wget https://github.com/hanni1s/IoTGuard/archive/refs/heads/main.zip
   unzip main.zip
   cd IoTGuard-main
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

### Step 4: Run IoTGuard! 🎉

```bash
streamlit run main.py
```

---

## Running IoTGuard

### First Time Setup:

1. **Register an account:**
   - Username: Your choice
   - Password: At least 8 characters with uppercase, lowercase, number, and special character
   - Example: `MyPass123!`

2. **Login:**
   - Use your new credentials
   - Choose "User" role

3. **Start scanning:**
   - Go to "Scan Device" tab
   - Enter an IP address (try `127.0.0.1` first - your own computer!)
   - Click "Start Scan"
   - Wait for results

### Tips for Scanning:

- **Test IP addresses:**
  - `127.0.0.1` - Your own computer (safe to test)
  - `192.168.1.1` - Usually your router
  - `192.168.1.x` - Devices on your network

- **Scan times:**
  - Simple devices: 10-30 seconds
  - Complex devices: 1-3 minutes

---

## 🐛 Troubleshooting

### Problem: "Python is not recognized"
**Solution (Windows):**
1. Uninstall Python
2. Reinstall and CHECK ✅ "Add Python to PATH"
3. Restart computer

### Problem: "pip is not recognized"
**Solution:**
```bash
# Windows:
python -m pip install --upgrade pip

# macOS/Linux:
python3 -m pip install --upgrade pip
```

### Problem: "Nmap not found"
**Solution:**
- Make sure Nmap is installed
- Restart your computer
- Try running Command Prompt/Terminal as Administrator

### Problem: "ModuleNotFoundError"
**Solution:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Problem: "Permission denied" (macOS/Linux)
**Solution:**
- Run Nmap commands with sudo:
```bash
sudo streamlit run main.py
```

### Problem: Scan shows "Unknown" for many ports
**Solution:**
- This is normal! Not all ports are in the database
- Use the "Research Port" links provided
- The system is designed to handle this gracefully

### Problem: Browser doesn't open automatically
**Solution:**
- Manually open your browser
- Go to: `http://localhost:8501`

---

## Need More Help?

### Common Issues:

**"It's too slow!"**
- First scan takes longer (building AI model)
- Subsequent scans are much faster
- Some devices have many ports and take longer

**"I forgot my password!"**
- Contact the project maintainer
- Or delete `iotguard.db` and start fresh (you'll lose scan history)

**"Scan fails!"**
- Check if target IP is correct
- Make sure device is online
- Some devices block scans (firewall)

### Getting Support:

- Check the [GitHub Issues](https://github.com/hanni1s/IoTGuard/issues)
- Read the main README.md
- Contact: [Project maintainer info]

---

## Installation Checklist

Before running IoTGuard, make sure you have:

- [ ] Python 3.8+ installed
- [ ] Nmap installed
- [ ] IoTGuard downloaded and extracted
- [ ] Dependencies installed (pip install -r requirements.txt)
- [ ] Can run: `streamlit run main.py`

If all checkboxes are ✅, you're ready to go! 🎉

---

## Learning Resources

**New to IoT Security?**
- IoTGuard is beginner-friendly!
- Start with simple scans (127.0.0.1)
- Read the port recommendations
- Learn from the AI risk assessments

**Want to Learn More?**
- Python: [python.org/about/gettingstarted](https://www.python.org/about/gettingstarted/)
- Network Security: Search "IoT security basics"
- Nmap: [nmap.org/book/man.html](https://nmap.org/book/man.html)

---

## ⚠️ Important Notes

1. **Only scan devices you own or have permission to scan**
   - Unauthorized scanning is illegal
   - IoTGuard is for educational purposes

2. **First scan takes longer**
   - The AI model needs to initialize
   - Subsequent scans are faster

3. **Some scans require admin/sudo**
   - Especially on macOS/Linux
   - This is normal for network scanning

4. **Firewall warnings**
   - Your computer may ask to allow Python/Nmap
   - Click "Allow" - this is necessary for scanning

---

## Yeay You're All Set!

Congratulations! You now have IoTGuard running on your computer! 

**Next steps:**
1. Create your account
2. Try scanning 127.0.0.1 (safe test)
3. Explore the features
4. Check out the beautiful dashboards
5. Generate reports!

**Have fun exploring IoT security!** 🛡️✨

---

<div align="center">

**Questions? Found a bug? Have suggestions?**

Visit the [GitHub Repository](https://github.com/hanni1s/IoTGuard)

</div>
