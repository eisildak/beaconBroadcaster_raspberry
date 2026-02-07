/**
 * Vercel Serverless Function for Zero-Click Deployment
 * Deploys Beacon Broadcaster to Raspberry Pi via SSH
 */

const { NodeSSH } = require('node-ssh');

// CORS headers for browser requests
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

/**
 * Main handler function
 */
module.exports = async (req, res) => {
  // Handle CORS preflight request
  if (req.method === 'OPTIONS') {
    return res.status(200).json({ ok: true });
  }

  // Only accept POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ 
      success: false, 
      error: 'Method not allowed. Use POST.' 
    });
  }

  // Parse request body
  const { ip, username, password, port = '22', directory = 'beacon_broadcaster' } = req.body;

  // Validate required fields
  if (!ip || !username || !password) {
    return res.status(400).json({
      success: false,
      error: 'Missing required fields: ip, username, password'
    });
  }

  // Validate IP address format
  const ipRegex = /^(\d{1,3}\.){3}\d{1,3}$/;
  if (!ipRegex.test(ip)) {
    return res.status(400).json({
      success: false,
      error: 'Invalid IP address format'
    });
  }

  const ssh = new NodeSSH();
  let connected = false;

  try {
    // Step 1: Connect to Raspberry Pi
    console.log(`[Deploy] Connecting to ${username}@${ip}:${port}...`);
    await ssh.connect({
      host: ip,
      username: username,
      password: password,
      port: parseInt(port),
      readyTimeout: 10000, // 10 seconds timeout
    });
    connected = true;
    console.log('[Deploy] ✅ SSH connection established');

    // Step 2: Create project directory
    console.log(`[Deploy] Creating directory: ${directory}`);
    await ssh.execCommand(`mkdir -p ${directory}`);

    // Step 3: Download and deploy files from GitHub
    const files = [
      'simulate_beacon.py',
      'index.html',
      'beacons_config.json',
      'run_detached.sh'
    ];

    const baseUrl = 'https://raw.githubusercontent.com/eisildak/beaconBroadcaster_raspberry/main/raspberry-pi-web-ui';

    for (const file of files) {
      console.log(`[Deploy] Downloading ${file}...`);
      const result = await ssh.execCommand(
        `curl -sL "${baseUrl}/${file}" -o "${directory}/${file}"`,
        { cwd: '~' }
      );

      if (result.code !== 0) {
        throw new Error(`Failed to download ${file}: ${result.stderr}`);
      }
      console.log(`[Deploy] ✅ ${file} deployed`);
    }

    // Step 4: Install Python dependencies
    console.log('[Deploy] Installing Python dependencies...');
    const pipResult = await ssh.execCommand(
      'pip3 install flask flask-cors 2>/dev/null || sudo pip3 install flask flask-cors',
      { cwd: directory }
    );
    console.log('[Deploy] ✅ Dependencies installed');

    // Step 5: Make run script executable and restart service
    console.log('[Deploy] Restarting beacon service...');
    await ssh.execCommand(`chmod +x ${directory}/run_detached.sh`);
    
    // Stop existing service
    await ssh.execCommand('screen -X -S beacon_simulator quit 2>/dev/null');
    
    // Start new service
    const startResult = await ssh.execCommand(
      `cd ${directory} && ./run_detached.sh`,
      { cwd: '~' }
    );
    
    console.log('[Deploy] ✅ Service restarted');

    // Step 6: Verify service is running
    const checkResult = await ssh.execCommand('screen -list | grep beacon_simulator');
    const isRunning = checkResult.code === 0;

    // Close SSH connection
    ssh.dispose();

    // Return success response
    return res.status(200).json({
      success: true,
      message: 'Deployment completed successfully!',
      details: {
        host: ip,
        directory: directory,
        filesDeployed: files,
        serviceRunning: isRunning,
        webUiUrl: `http://${ip}:5000`
      }
    });

  } catch (error) {
    console.error('[Deploy] ❌ Error:', error.message);

    // Close SSH connection if still open
    if (connected) {
      ssh.dispose();
    }

    // Determine error type and appropriate status code
    let statusCode = 500;
    let errorMessage = error.message;

    if (error.message.includes('ENOTFOUND') || error.message.includes('ETIMEDOUT')) {
      statusCode = 503;
      errorMessage = `Cannot reach Raspberry Pi at ${ip}. Check IP address and network connection.`;
    } else if (error.message.includes('authentication') || error.message.includes('password')) {
      statusCode = 401;
      errorMessage = 'SSH authentication failed. Check username and password.';
    } else if (error.message.includes('ECONNREFUSED')) {
      statusCode = 503;
      errorMessage = `SSH connection refused. Check if SSH is enabled on port ${port}.`;
    }

    return res.status(statusCode).json({
      success: false,
      error: errorMessage,
      details: {
        host: ip,
        port: port,
        directory: directory
      }
    });
  }
};
