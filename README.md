# 🧹 Bat Broom - Windows Temporary Files Cleanup GUI

A user-friendly Python GUI application for safely cleaning Windows temporary files and system cache.

## Features

- **🎯 Selective Cleanup**: Choose exactly which temporary files to clean
- **📁 Organized Sections**: Files grouped by type (User Temp, System, Browser, etc.)
- **✅ Checkbox Interface**: Easy selection with section-level and individual file controls
- **📊 Real-time Logging**: See exactly what's being cleaned in real-time
- **🔒 Safe Operations**: Built-in error handling and permission checks
- **👑 Admin Detection**: Automatically detects and warns about administrator privileges
- **🧵 Threaded Operations**: Non-blocking UI during cleanup operations

## Screenshots

```
┌─────────────────────────────────────────────────────┐
│                🧹 Bat Broom                         │
│         Windows Temporary Files Cleanup Tool        │
├─────────────────────┬───────────────────────────────┤
│ Cleanup Sections    │ [Select All] [Deselect All]  │
│                     │ [🧹 Start Cleanup]           │
│ ☑ User Temporary    │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│   ☑ User Temp Dir   │                               │
│   ☑ AppData Temp    │ Cleanup Log                   │
│   ☐ Internet Cache  │ ┌─────────────────────────────┐ │
│                     │ │[12:34:56] Starting cleanup │ │
│ ☐ System Files     │ │[12:34:57] ✅ User Temp -   │ │
│ ☐ Browser Cache    │ │          Cleaned (45 items)│ │
│ ☐ Crash Dumps      │ │[12:34:58] ℹ️ Chrome Cache  │ │
│                     │ │          - No files found  │ │
│                     │ └─────────────────────────────┘ │
└─────────────────────┴───────────────────────────────┘
```

## Installation & Usage

### Prerequisites
- Python 3.6 or higher
- Windows operating system
- Administrator privileges (recommended)

### Quick Start

1. **Download the application:**
   ```bash
   # Clone or download the files
   git clone <repository-url>
   cd bat-broom
   ```

2. **Run the application:**
   ```bash
   python bat_broom.py
   ```

3. **For best results, run as administrator:**
   - Right-click on Command Prompt
   - Select "Run as administrator"
   - Navigate to the application folder
   - Run: `python bat_broom.py`

### Creating an Executable (Optional)

To create a standalone executable:

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Create executable:**
   ```bash
   pyinstaller --onefile --windowed --name="BatBroom" bat_broom.py
   ```

3. **Find the executable in the `dist` folder**

## Cleanup Sections

### 🏠 User Temporary Files
- User Temp Directory
- AppData Local Temp
- Internet Temporary Files
- Internet Cache & Cookies
- Web Cache

### 🖥️ System Temporary Files
- System Temp Directory
- Prefetch Files
- Windows Update Downloads

### 📄 Recent Files and History
- Recent Documents
- Recent Files (Legacy)

### 💥 Crash Dumps and Logs
- User Crash Dumps
- System Logs
- Debug Files

### 📱 Application Specific
- UWP App Temp State
- Explorer Thumbnails
- Icon Cache
- Windows Caches

### 🌐 Browser Temporary Files
- Chrome Cache & Code Cache
- Firefox Cache
- Edge Cache

## Safety Features

- **✅ Path Validation**: Checks if paths exist before attempting deletion
- **🔒 Permission Handling**: Gracefully handles access denied errors
- **📝 Detailed Logging**: Shows exactly what was cleaned and any issues
- **⚠️ Safe Defaults**: Only cleans temporary files, never user data
- **🛡️ Error Recovery**: Continues operation even if some files can't be deleted

## Usage Tips

1. **Run as Administrator**: For system-level cleanup operations
2. **Select Carefully**: Only choose sections you want to clean
3. **Check the Log**: Review what was cleaned after each operation
4. **Close Browsers**: Close web browsers before cleaning browser caches
5. **Regular Maintenance**: Run weekly or monthly for best results

## Troubleshooting

### Common Issues

**"Access Denied" errors:**
- Run the application as administrator
- Close programs that might be using the files
- Some system files cannot be deleted while Windows is running (this is normal)

**"Path not found" errors:**
- This is normal - not all paths exist on every system
- The application will skip non-existent paths safely

**Application won't start:**
- Ensure Python 3.6+ is installed
- Check that tkinter is available: `python -c "import tkinter"`

### Performance Notes

- Cleanup operations run in a separate thread to keep the UI responsive
- Large caches (like browser caches) may take longer to clean
- Progress is shown in real-time in the log window

## Technical Details

- **Language**: Python 3.6+
- **GUI Framework**: tkinter (included with Python)
- **Threading**: Uses threading for non-blocking operations
- **Platform**: Windows-specific paths and operations
- **Dependencies**: No external dependencies required

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## Disclaimer

This application is designed to safely clean temporary files. While it includes safety measures, please:
- Review selected paths before cleaning
- Ensure you have backups of important data
- Test on a non-critical system first
- Use at your own risk

---

**Happy Cleaning! 🧹** 