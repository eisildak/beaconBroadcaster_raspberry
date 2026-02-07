# Code Guidelines & Development Rules

## 📋 General Principles

### Language Policy
- ✅ **Always use English** for all code, comments, documentation, and UI text
- ✅ **Variable names** must be in English and follow camelCase convention
- ✅ **Function names** must be descriptive and in English
- ✅ **Comments** must be in English only
- ❌ **No Turkish or other languages** in codebase (except in README examples for localization demos)

### Code Style

#### JavaScript/HTML
- Use **camelCase** for JavaScript variables and functions
  ```javascript
  // ✅ Good
  const currentBeacon = null;
  async function enableBeacon(index) { }
  
  // ❌ Bad
  const current_beacon = null;
  async function enable_beacon(index) { }
  ```

- Use **descriptive names**
  ```javascript
  // ✅ Good
  const savedBeacons = [];
  function updateCurrentBeaconUI() { }
  
  // ❌ Bad
  const arr = [];
  function update() { }
  ```

- **Comments should explain WHY, not WHAT**
  ```javascript
  // ✅ Good
  // Refresh every 3 seconds to catch manual backend changes
  setInterval(checkCurrentBeacon, 3000);
  
  // ❌ Bad
  // Set interval
  setInterval(checkCurrentBeacon, 3000);
  ```

#### Python
- Follow **PEP 8** style guide
- Use **snake_case** for functions and variables
  ```python
  # ✅ Good
  def start_ibeacon(uuid, major, minor):
      current_beacon = None
  
  # ❌ Bad
  def StartIbeacon(uuid, major, minor):
      currentBeacon = None
  ```

- Add **docstrings** for functions
  ```python
  def enable_beacon(uuid, major, minor):
      """Enable beacon broadcasting with specified parameters.
      
      Args:
          uuid: Beacon UUID string
          major: Major version (0-65535)
          minor: Minor version (0-65535)
      
      Returns:
          bool: True if successful, False otherwise
      """
  ```

### UI/UX Guidelines

#### Consistency
- Use **consistent terminology** across the application
  - "Beacon" not "iBeacon" or "Signal"
  - "Broadcasting" not "Transmitting" or "Emitting"
  - "Enable/Disable" not "Start/Stop" or "On/Off"

#### User Feedback
- Always provide **visual feedback** for user actions
  ```javascript
  // ✅ Good - Show notification
  showMessage('Beacon saved successfully.');
  
  // ❌ Bad - Silent operation
  await fetch(`${API_BASE}/beacon/add`, ...);
  ```

- Use **loading states** for async operations
- Display **error messages** that are actionable

#### Accessibility
- Use **semantic HTML** elements
- Include **alt text** for images
- Ensure **keyboard navigation** works
- Maintain **color contrast** ratios (WCAG AA minimum)

### API Design

#### Endpoints
- Use **RESTful conventions**
  ```
  GET  /beacon              - Get current beacon
  GET  /beacon/list         - List all saved beacons
  POST /beacon/add          - Add new beacon
  GET  /beacon/enable/...   - Enable beacon (legacy Appium)
  GET  /beacon/disable      - Disable beacon (legacy Appium)
  DELETE /beacon/delete/:id - Delete beacon
  ```

- Return **appropriate HTTP status codes**
  - 200: Success
  - 400: Bad request
  - 500: Server error

- Use **consistent JSON response format**
  ```json
  {
    "status": "success",
    "data": { ... }
  }
  ```

### Error Handling

#### Frontend
- **Always wrap async calls** in try-catch
  ```javascript
  // ✅ Good
  try {
      const response = await fetch(url);
      if (!response.ok) throw new Error('API error');
      // Handle response
  } catch (error) {
      console.error('Operation failed:', error);
      showMessage('Failed to complete operation', 'error');
  }
  
  // ❌ Bad
  const response = await fetch(url);
  const data = await response.json();
  ```

- **Log errors to console** for debugging
- **Show user-friendly messages** (not technical errors)

#### Backend
- **Validate input parameters**
- **Log errors with context**
  ```python
  try:
      result = start_ibeacon(uuid, major, minor)
  except Exception as e:
      print(f"❌ Failed to enable beacon {uuid}: {e}")
      return jsonify({'error': str(e)}), 500
  ```

### Git Commit Messages

- Use **conventional commits** format:
  ```
  feat: Add beacon preset functionality
  fix: Resolve stop button not working
  docs: Update API reference
  style: Modernize UI with Tailwind
  refactor: Simplify beacon rendering logic
  test: Add unit tests for beacon management
  ```

- Keep first line **under 72 characters**
- Add **detailed description** if needed

### File Organization

```
raspberry-pi-web-ui/
├── index.html              # Main UI (single file for simplicity)
├── simulate_beacon.py      # Backend API
├── beacons_config.json     # Persistent beacon storage
├── auto-deployer.py        # Deployment tool
├── assets/
│   └── play_store_512.png  # Logo and images
└── README.md               # Detailed documentation
```

### Testing Requirements

- **Test all user workflows** manually before committing
  1. Add beacon
  2. Enable beacon
  3. Verify beacon is broadcasting
  4. Stop beacon
  5. Delete beacon

- **Test error cases**
  - Network disconnection
  - Invalid input
  - Backend errors

- **Test on actual hardware** (Raspberry Pi) before tagging releases

### Deployment

- **Never deploy untested code** to production
- **Create backup** before deploying
  ```bash
  cp simulate_beacon.py simulate_beacon.py.backup_$(date +%Y%m%d_%H%M%S)
  ```

- **Verify deployment** before marking as complete
  ```bash
  curl http://RASPBERRY_PI_IP:8000/beacon
  ```

### Documentation

- **Keep README.md updated** with new features
- **Document API changes** immediately
- **Add inline comments** for complex logic
- **Update version numbers** in footer/header

### Security

- **Never commit sensitive data**
  - No hardcoded passwords
  - No API keys
  - No production credentials

- **Sanitize user input** before using
  ```python
  # Validate UUID format
  if not re.match(r'^[0-9a-fA-F-]{36}$', uuid):
      return jsonify({'error': 'Invalid UUID'}), 400
  ```

- **Use HTTPS** in production (if exposed to internet)

### Performance

- **Minimize API calls**
  - Cache data when possible
  - Use debouncing for rapid actions

- **Optimize refresh intervals**
  - 3 seconds is acceptable for status polling
  - Avoid polling if using WebSockets

- **Lazy load** large resources

## 🚀 Quick Reference

### Before Committing
- [ ] All text is in English
- [ ] Code follows style guidelines
- [ ] Error handling is present
- [ ] Console has no errors
- [ ] Tested on actual device (if UI changes)
- [ ] Commit message is descriptive

### Before Deploying
- [ ] Backup created
- [ ] Tested on local Raspberry Pi
- [ ] Documentation updated
- [ ] Version number bumped
- [ ] Deployment script verified

---

**Last Updated:** February 8, 2026  
**Version:** 2.0
