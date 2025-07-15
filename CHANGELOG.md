# Changelog

All notable changes to Bat Broom will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-XX

### Added
- Initial release of Bat Broom GUI application
- Windows temporary files cleanup functionality
- Organized cleanup sections with checkboxes
- Real-time logging and progress indication
- Administrator privilege detection
- Safe file deletion with error handling
- Threaded operations for responsive UI
- Comprehensive cleanup categories:
  - User Temporary Files
  - System Temporary Files  
  - Recent Files and History
  - Crash Dumps and Logs
  - Application Specific files
  - Browser Temporary Files
- Select All/Deselect All functionality
- Confirmation dialogs for safety
- Status bar and progress feedback
- Detailed cleanup logging with timestamps

### Security
- Safe path validation before deletion
- Permission error handling
- Administrator privilege warnings
- Confirmation dialogs for destructive operations

## [Unreleased]

### Planned
- Additional cleanup categories
- Settings/preferences system
- Scheduled cleanup functionality
- Export cleanup reports 