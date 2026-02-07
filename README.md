# 🎯 Beacon Broadcaster Raspberry

![Platform](https://img.shields.io/badge/platform-Raspberry_Pi-red)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-green)
![License](https://img.shields.io/badge/license-MIT-green)

**Professional iBeacon broadcaster for Raspberry Pi with modern web interface**

Real iBeacon broadcasting solution that actually works! Control multiple beacons from your browser with automatic deployment for any Raspberry Pi.

---

## ⭐ Key Features

- 🚀 **One-Click Auto Deployment** - Browser-based installer, no manual steps
- 🌐 **Modern Web UI** - Control beacons from any device on your network
- 📡 **Real iBeacon Broadcasting** - Visible to all iOS/Android scanner apps
- 💾 **Beacon Presets** - Save and manage multiple beacon configurations
- 🔄 **Instant Enable/Disable** - Start/stop beacons with one click
- 👥 **Universal Setup** - Anyone can use with their own Raspberry Pi
- ✅ **Appium Compatible** - All existing test automation continues working
- 🔒 **Safe Deployment** - Automatic backups, easy rollback

---

## 🚀 Quick Start (Zero Install!)

### ✨ Recommended: Setup Wizard (No Installation Required)

🔗 **[Open Setup Wizard on GitHub Pages](https://eisildak.github.io/beaconBroadcaster_raspberry/setup-wizard.html)**

**3 Simple Steps:**
1. Enter your Raspberry Pi IP, username, password
2. Click "Generate Deployment Package"
3. Download and run the deployment script

**That's it!** ☕ Grab a coffee while it deploys automatically.  
🌐 **Web UI opens automatically** in your browser when deployment completes!

✅ Works entirely in your browser  
✅ No Python, Flask, or repo cloning needed  
✅ Anyone can use without any setup

---

### 🔧 Alternative: Auto Deployer (Local Deployment)

For developers who prefer running deployment tools locally with instant visual feedback:

**Step 1:** Clone repository
```bash
git clone https://github.com/eisildak/beaconBroadcaster_raspberry.git
cd beaconBroadcaster_raspberry
```

**Step 2:** Install Flask
```bash
pip3 install flask
```

**Step 3:** Launch Auto Deployer
```bash
cd raspberry-pi-web-ui
python3 auto-deployer.py
```

**Then open `http://localhost:5000` or visit:** `file:///path/to/repo/index.html`  
(localhost index.html auto-redirects to Auto Deployer)

📤 **Fill in your Raspberry Pi details** → Click Deploy → **Web UI opens automatically!**

---

## ❓ FAQ

### Can I use this without the repo on Raspberry Pi?

**Yes!** Both methods create everything automatically:

- **Auto Deployer**: Uploads all files via SSH - no existing repo needed
- **Setup Wizard**: Generates complete deployment package from scratch

**Only requirement**: SSH access to your Raspberry Pi. The system handles the rest.

### Does this break existing Appium tests?

**No** - 100% backward compatible:
- All existing API endpoints unchanged  
- Original file backed up automatically
- Easy rollback anytime
- Test automation continues working

### Can I test without cloning the repo?

**Yes!** Use the GitHub Pages hosted version:
```
https://eisildak.github.io/beaconBroadcaster_raspberry/setup-wizard.html
```

Runs entirely in browser - no installation needed!

### Is my data private and secure?

**Yes!** Your sensitive information is protected:
- ✅ SSH credentials never leave your browser
- ✅ IP addresses and passwords are NOT stored in the repository
- ✅ `beacons_config.json` (your beacon data) is gitignored
- ✅ All sensitive files automatically excluded from version control

**Safe to fork:** The `.gitignore` file ensures your private configuration stays local.

---

## 🌐 GitHub Pages Setup

Host the setup wizard for your team:

1. **Repository Settings** → **Pages**
2. Set **Source** to `main` branch, `/ (root)` folder (or move files from `docs/` to root)
3. Save and deploy
4. Share: `https://eisildak.github.io/beaconBroadcaster_raspberry/`

The wizard is pure HTML/JavaScript - no server required!

---

## 📱 Web UI Features

### 🎯 Beacon Management

**Add Beacon Presets:**
- Custom Name (e.g., "Office Entrance", "Meeting Room A")
- UUID Configuration
- Major/Minor Values (0-65535)
- TX Power Settings
- One-click save to persistent storage

**Manage Beacons:**
- ▶️ **Enable** - Start broadcasting with one click
- 🛑 **Stop** - Disable active beacon
- 🗑️ **Delete** - Remove saved beacon
- 📊 **Real-time Status** - See which beacon is broadcasting
- 💾 **Persistent Storage** - Beacons saved even after reboot

### 🌐 Access from Anywhere

- Connect from any device on your network
- Modern responsive design (works on phone/tablet)
- Dark mode interface
- Real-time status updates every 3 seconds

---

## 🔧 Appium Integration

All existing API endpoints work exactly as before! Your test automation continues without any changes.

### Python Example

```python
import requests

BASE_URL = "http://YOUR_RASPBERRY_PI_IP:8000"

def test_proximity_feature():
    # Enable beacon before test
    requests.get(f"{BASE_URL}/beacon/enable/FDA50693-A4E2-4FB1-AFCF-C6EB07647825/100/1")
    
    # Run your test
    # ... test code ...
    
    # Disable beacon after test
    requests.get(f"{BASE_URL}/beacon/disable")
```

### JavaScript/Node.js Example

```javascript
const axios = require('axios');
const BASE_URL = 'http://YOUR_RASPBERRY_PI_IP:8000';

beforeEach(async () => {
    await axios.get(`${BASE_URL}/beacon/enable/FDA50693-A4E2-4FB1-AFCF-C6EB07647825/100/1`);
});

afterEach(async () => {
    await axios.get(`${BASE_URL}/beacon/disable`);
});
```

---

## 🎮 Use Cases

- ✅ **Mobile App Testing** - Test location-based features
- ✅ **QA Automation** - Integrate with Appium/Selenium tests
- ✅ **Indoor Positioning** - Simulate beacon infrastructure
- ✅ **Proximity Marketing** - Test beacon campaigns
- ✅ **Development** - Quick beacon configuration changes
- ✅ **Demonstration** - Show beacon features to stakeholders

---

## 📋 Requirements

### Hardware
- Raspberry Pi (any model with Bluetooth)
- Already running beacon simulator
- Network connection

### Software
- Python 3.x (on your Mac for deployment tool)
- Flask (`pip3 install flask`)
- sshpass (`brew install hudochenkov/sshpass/sshpass`) - Optional for auto-deploy

---

## 👥 Multi-User Support

**Everyone can use with their own Raspberry Pi!**

The setup wizard generates custom deployment packages for each user:
- Enter YOUR Raspberry Pi IP, username, password
- Download personalized deployment script
- Deploy to YOUR Raspberry Pi
- Access YOUR web UI

Perfect for teams where each person has their own test Raspberry Pi!

---

## 🔒 Safety Features

✅ **Automatic Backups** - Original files backed up before deployment  
✅ **Easy Rollback** - Restore previous version with one command  
✅ **Backward Compatible** - All existing Appium APIs unchanged  
✅ **Non-Destructive** - Existing beacon configurations preserved  

### Rollback Instructions

If you need to revert:

```bash
ssh your_user@your_raspberry_pi_ip
cd pointr-beacon-simulator
screen -X -S beacon_simulator quit
cp simulate_beacon.py.backup_* simulate_beacon.py
./run_detached.sh
```

---

## 📞 API Reference

### Existing Endpoints (Appium-Compatible)

```bash
# Enable beacon
GET /beacon/enable/<uuid>/<major>/<minor>?rssi=-59

# Disable beacon
GET /beacon/disable

# Get current beacon status
GET /beacon

# USB beacon control (if applicable)
GET /beacon/usb/enable
GET /beacon/usb/disable
GET /beacon/usb
```

### New Web UI Endpoints

```bash
# List saved beacons
GET /beacon/list

# Add beacon preset
POST /beacon/add
Body: {"name": "...", "uuid": "...", "major": 1, "minor": 1, "rssi": -59}

# Delete beacon preset
DELETE /beacon/delete/<index>

# Web interface
GET /
```

---

## 🐛 Troubleshooting

### Auto-deployer won't start

```bash
# Install Flask
pip3 install flask

# Check Python version
python3 --version  # Should be 3.6+
```

### Can't connect to Raspberry Pi

```bash
# Test SSH connection
ssh your_user@your_ip

# Check if beacon service is running
ssh your_user@your_ip "screen -list"
```

### Web UI not accessible

```bash
# Check if service is running on Pi
curl http://YOUR_IP:8000/beacon

# Restart beacon service
ssh your_user@your_ip
cd pointr-beacon-simulator
screen -X -S beacon_simulator quit
./run_detached.sh
```

---

## 📖 Documentation

- **raspberry-pi-web-ui/README.md** - Detailed web UI documentation
- **raspberry-pi-web-ui/BAŞLANGIÇ_KILAVUZU.md** - Turkish quick start guide
- **raspberry-pi-web-ui/WEB_UI_DEPLOYMENT.md** - Manual deployment guide
- **MACOS_PROJECT_BACKUP.md** - Historical macOS attempts (for reference)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Flask - Web framework
- Raspberry Pi Foundation
- Original beacon simulator: [pointrlabs/ptr-raspberry-pi-beacon-simulator](https://github.com/pointrlabs/ptr-raspberry-pi-beacon-simulator)

---

## 👨‍💻 Author

**Erol İşıldak** - Mobile QA Engineer & Developer

Built for the mobile testing community with ❤️

---

**Why Raspberry Pi Instead of macOS?**

macOS 26.1+ blocks BLE peripheral advertising due to security policies. Even with Bleno/HCI access or Swift/CoreBluetooth, beacons are not visible to standard scanner apps. Raspberry Pi with Linux/BlueZ stack broadcasts real iBeacon signals that work with all iOS/Android apps.

See `MACOS_PROJECT_BACKUP.md` for details on macOS limitations.
