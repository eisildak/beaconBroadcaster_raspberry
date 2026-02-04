# Beacon Broadcaster Pro

![Platform](https://img.shields.io/badge/platform-macOS-blue)
![SwiftUI](https://img.shields.io/badge/SwiftUI-5.0+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Professional iBeacon broadcaster for macOS - Now with Menu Bar integration**

Beacon Broadcaster Pro is a native macOS application designed for mobile developers and QA engineers to simulate BLE beacon signals directly from Mac computers. Built with SwiftUI and modern macOS features.

## ✨ Features

- 🎯 **Menu Bar App** - Runs quietly in the background, accessible from the macOS menu bar
- 🔄 **Multiple Beacon Management** - Create and manage multiple beacon configurations
- ⚙️ **Full Customization** - Configure UUID, Major, Minor values and TX Power
- ⚡ **Instant Broadcasting** - Start/stop beacon advertising with a single click
- 💾 **Persistent Storage** - Automatically saves all beacon configurations
- 🎨 **Native macOS UI** - Beautiful SwiftUI interface with Dark Mode support
- ✅ **Form Validation** - Real-time validation for all beacon parameters
- 📊 **Status Indicators** - Visual feedback for broadcasting status
- 🔍 **Search & Filter** - Quick search through beacon configurations

## 🚀 Use Cases

- Testing location-based triggers in mobile applications
- QA validation of proximity features  
- Bluetooth Low Energy (BLE) experimentation
- iBeacon protocol development
- Indoor positioning system testing

## 📋 Requirements

- macOS 11.0 or later
- Bluetooth 4.0 (BLE) support
- Xcode 15+ (for development)

## 🛠️ Installation

### Build from Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/beacon-broadcaster-pro.git
cd beacon-broadcaster-pro
```

2. Open in Xcode:
```bash
open BeaconBroadcasterPro/BeaconBroadcasterPro.xcodeproj
```

3. Build and run (⌘R)

## 📱 Usage

### Menu Bar Mode
1. Launch the app - it appears in your menu bar with a beacon icon
2. Click the menu bar icon to access quick controls
3. Select a beacon to start/stop broadcasting
4. Click "Open App" for full configuration interface

### Main Application
1. Click "Add Beacon" to create a new beacon configuration
2. Configure UUID, Major, Minor values
3. Select the beacon from the list
4. Click "Start Broadcasting"
5. Use "Stop Broadcasting" when done

## 🔧 Configuration

The app supports standard iBeacon parameters:

- **UUID**: 128-bit identifier (e.g., `FDA50693-A4E2-4FB1-AFCF-C6EB07647825`)
- **Major**: 16-bit unsigned integer (0-65535)
- **Minor**: 16-bit unsigned integer (0-65535)
- **TX Power**: Transmission power in dBm (-100 to 20)

### Form Validation
- Real-time UUID format validation
- Major/Minor range checking
- TX Power validation
- Helpful error messages

## 🏗️ Technical Architecture

- **SwiftUI** - Modern declarative UI framework
- **CoreBluetooth** - BLE peripheral management
- **UserDefaults** - Persistent beacon storage
- **Combine** - Reactive state management
- **AppKit** - Menu bar integration (NSStatusBar)

## 🔐 Permissions

This app requires:
- **Bluetooth Access** - For broadcasting beacon signals

All permissions are requested through standard macOS privacy prompts.

## ⚠️ CRITICAL LIMITATION

**macOS CANNOT broadcast real iBeacon signals!**

Due to macOS CoreBluetooth API restrictions:
- ❌ **NOT compatible with standard iBeacon scanners/apps**
- ❌ **Indoor positioning apps WILL NOT detect these signals**
- ❌ **Location-based triggers WILL NOT work**
- ❌ Cannot broadcast Apple Manufacturer Data (0x4C00)
- ❌ CLBeaconRegion broadcasting not available on macOS
- ✅ Only broadcasts BLE Service UUIDs (detectable by LightBlue/nRF Connect)

**This is a macOS operating system limitation, not a bug.**

### ✅ For REAL iBeacon Broadcasting:
1. **Use iOS** - iPhone/iPad support native iBeacon broadcasting
2. **Use dedicated beacon hardware** - Physical beacon devices
3. **Use Raspberry Pi + Linux** - BlueZ stack supports manufacturer data
4. **Use ESP32/Arduino** - DIY beacon hardware

### 🎯 What This App IS Good For:
- Learning BLE peripheral concepts
- Testing BLE scanner apps (LightBlue, nRF Connect)
- Understanding beacon data structures
- Development/experimentation only

## 🧪 Testing

Test with these scanner apps:
- **LightBlue** (iOS/macOS) - Recommended
- **nRF Connect** (iOS/Android)
- **BLE Scanner** (Android)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Erol** - Mobile QA Engineer & Developer

## 🙏 Acknowledgments

- Apple Core Bluetooth Framework
- SwiftUI Team
- Flutter Beacon Broadcaster inspiration

## 📞 Support

For bugs, feature requests, or questions:
- Open an issue on GitHub
- Email: your.email@example.com

---

**Made with ❤️ for the mobile development community**
