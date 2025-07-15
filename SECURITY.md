# Security Policy

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in Bat Broom, please report it responsibly:

### How to Report

1. **Do not** create a public GitHub issue for security vulnerabilities
2. Email the maintainers directly (if available) or create a private security advisory
3. Include the following information:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- We will acknowledge receipt of your report within 48 hours
- We will investigate and provide an initial assessment within 1 week
- We will work with you to understand and resolve the issue
- We will credit you for the discovery (unless you prefer to remain anonymous)

### Security Considerations

Bat Broom is designed with security in mind:

- **File Deletion**: Only deletes temporary files, never user data
- **Path Validation**: Validates all paths before deletion attempts
- **Permission Handling**: Gracefully handles permission errors
- **Administrator Checks**: Warns users about privilege requirements
- **Safe Defaults**: Conservative cleanup selections by default

### Responsible Disclosure

We follow responsible disclosure practices:

- Security fixes will be released as soon as possible
- We will coordinate with reporters on disclosure timing
- We will provide credit to security researchers
- We will maintain a security advisory for significant issues

Thank you for helping keep Bat Broom secure! 