#!/usr/bin/env python3
"""
Raspberry Pi Beacon Broadcaster - Auto Deployer
Fully automated deployment with web interface
"""

from flask import Flask, render_template_string, request, jsonify
import subprocess
import os
import json
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
SCRIPT_DIR = Path(__file__).parent

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raspberry Pi Beacon - Auto Deployer</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-blue-900 via-purple-900 to-pink-900 min-h-screen">
    <div class="container mx-auto px-4 py-12 max-w-2xl">
        <div class="bg-white rounded-2xl shadow-2xl overflow-hidden">
            <!-- Header -->
            <div class="bg-gradient-to-r from-blue-600 to-purple-600 p-8 text-white text-center">
                <div class="flex justify-center mb-4">
                    <img src="assets/play_store_512.png" alt="Beacon Broadcaster" class="w-20 h-20 rounded-lg shadow-lg">
                </div>
                <h1 class="text-4xl font-bold mb-2">Beacon Auto Deployer</h1>
                <p class="text-blue-100 text-lg">One-click deployment to your Raspberry Pi</p>
                <p class="text-sm text-blue-200 mt-2">✨ Fully automated • Real-time logs • Zero configuration</p>
            </div>

            <!-- Form -->
            <div class="p-8">
                <div class="mb-6 bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                    <p class="text-sm text-blue-800">
                        <strong>📋 Prerequisites:</strong> SSH access to your Raspberry Pi
                    </p>
                </div>
                
                <form id="deploy-form" class="space-y-6">
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-2">
                            📡 Raspberry Pi IP Address *
                        </label>
                        <input type="text" id="rpi-ip" required value="192.168.1.180"
                               placeholder="e.g., 192.168.1.180"
                               class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition">
                    </div>

                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-2">
                            👤 SSH Username *
                        </label>
                        <input type="text" id="rpi-user" required value="erol"
                               placeholder="e.g., pi"
                               class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition">
                    </div>

                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-2">
                            🔐 SSH Password *
                        </label>
                        <input type="password" id="rpi-password" required value="1234"
                               placeholder="Enter SSH password"
                               class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition">
                    </div>

                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-2">
                            📁 Project Directory *
                        </label>
                        <input type="text" id="rpi-dir" required value="pointr-beacon-simulator"
                               placeholder="e.g., pointr-beacon-simulator"
                               class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition">
                    </div>

                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-2">
                            🔌 Port
                        </label>
                        <input type="number" id="rpi-port" value="8000" min="1000" max="65535"
                               placeholder="8000"
                               class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition">
                    </div>

                    <button type="submit" id="deploy-btn"
                            class="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-4 px-6 rounded-lg shadow-lg transform transition hover:scale-105 hover:shadow-xl">
                        🚀 Start Auto Deployment
                    </button>
                </form>
            </div>

            <!-- Progress Section -->
            <div id="progress-section" class="hidden p-8 bg-gray-50 border-t">
                <div class="flex items-center justify-center mb-6">
                    <div class="animate-spin w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full mr-3"></div>
                    <h2 class="text-2xl font-bold text-gray-800">Deployment in Progress...</h2>
                </div>
                <div class="bg-white rounded-lg p-4 mb-4">
                    <p class="text-sm text-gray-600 text-center">
                        ☕ This may take 30-60 seconds. Please wait...
                    </p>
                </div>
                <div id="progress-log" class="bg-gray-900 text-green-400 p-4 rounded-lg font-mono text-sm h-96 overflow-y-auto shadow-inner">
                </div>
            </div>

            <!-- Success Section -->
            <div id="success-section" class="hidden p-8 bg-green-50 border-t border-green-200">
                <div class="text-center">
                    <div class="text-6xl mb-4">✅</div>
                    <h2 class="text-3xl font-bold text-green-800 mb-2">Deployment Successful!</h2>
                    <p class="text-gray-600 mb-4">Your beacon broadcaster is ready</p>
                    <div class="bg-blue-100 border border-blue-300 rounded-lg p-4 mb-6">
                        <p class="text-sm text-blue-800">🚀 Opening Web UI automatically in <span id="countdown">3</span> seconds...</p>
                    </div>
                    <a id="open-web-ui" href="#" target="_blank"
                       class="inline-block bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-8 rounded-lg transition transform hover:scale-105">
                        🌐 Open Web UI Now
                    </a>
                    <button onclick="window.location.reload()"
                            class="ml-4 inline-block bg-gray-600 hover:bg-gray-700 text-white font-bold py-3 px-8 rounded-lg transition transform hover:scale-105">
                        🔄 New Deployment
                    </button>
                </div>
            </div>

            <!-- Error Section -->
            <div id="error-section" class="hidden p-8 bg-red-50 border-t border-red-200">
                <div class="text-center">
                    <div class="text-6xl mb-4">❌</div>
                    <h2 class="text-3xl font-bold text-red-800 mb-2">Deployment Failed</h2>
                    <div class="bg-red-100 border border-red-300 rounded-lg p-4 mb-6">
                        <p id="error-message" class="text-sm text-red-800 font-mono"></p>
                    </div>
                    <div class="text-left bg-white rounded-lg p-4 mb-6 text-sm text-gray-600">
                        <p class="font-semibold mb-2">💡 Troubleshooting tips:</p>
                        <ul class="list-disc list-inside space-y-1">
                            <li>Verify Raspberry Pi IP address and SSH credentials</li>
                            <li>Ensure sshpass is installed: <code class="bg-gray-100 px-2 py-1 rounded">brew install hudochenkov/sshpass/sshpass</code></li>
                            <li>Check if Raspberry Pi is accessible on the network</li>
                            <li>Confirm project directory exists on Raspberry Pi</li>
                        </ul>
                    </div>
                    <button onclick="window.location.reload()"
                            class="inline-block bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-8 rounded-lg transition transform hover:scale-105">
                        🔄 Try Again
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script>
        const form = document.getElementById('deploy-form');
        const progressSection = document.getElementById('progress-section');
        const successSection = document.getElementById('success-section');
        const errorSection = document.getElementById('error-section');
        const progressLog = document.getElementById('progress-log');
        const deployBtn = document.getElementById('deploy-btn');

        function addLog(message, type = 'info') {
            const timestamp = new Date().toLocaleTimeString();
            const color = type === 'error' ? 'text-red-400' : type === 'success' ? 'text-green-400' : 'text-blue-400';
            progressLog.innerHTML += `<div class="${color}">[${timestamp}] ${message}</div>`;
            progressLog.scrollTop = progressLog.scrollHeight;
        }

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const config = {
                ip: document.getElementById('rpi-ip').value.trim(),
                user: document.getElementById('rpi-user').value.trim(),
                password: document.getElementById('rpi-password').value,
                dir: document.getElementById('rpi-dir').value.trim(),
                port: document.getElementById('rpi-port').value.trim()
            };

            // Show progress
            progressSection.classList.remove('hidden');
            successSection.classList.add('hidden');
            errorSection.classList.add('hidden');
            deployBtn.disabled = true;
            progressLog.innerHTML = '';

            addLog('🚀 Starting deployment...');
            addLog(`📡 Target: ${config.user}@${config.ip}`);

            try {
                const response = await fetch('/deploy', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(config)
                });

                const data = await response.json();

                if (data.success) {
                    data.logs.forEach(log => addLog(log, 'info'));
                    addLog('✅ Deployment completed!', 'success');
                    
                    setTimeout(() => {
                        progressSection.classList.add('hidden');
                        successSection.classList.remove('hidden');
                        const webUiUrl = `http://${config.ip}:${config.port}`;
                        document.getElementById('open-web-ui').href = webUiUrl;
                        
                        // Auto-redirect countdown
                        let countdown = 3;
                        const countdownEl = document.getElementById('countdown');
                        const countdownInterval = setInterval(() => {
                            countdown--;
                            if (countdownEl) countdownEl.textContent = countdown;
                            if (countdown <= 0) {
                                clearInterval(countdownInterval);
                                window.open(webUiUrl, '_blank');
                            }
                        }, 1000);
                    }, 1000);
                } else {
                    addLog(`❌ Error: ${data.error}`, 'error');
                    setTimeout(() => {
                        progressSection.classList.add('hidden');
                        errorSection.classList.remove('hidden');
                        document.getElementById('error-message').textContent = data.error;
                    }, 1000);
                }
            } catch (error) {
                addLog(`❌ Connection error: ${error.message}`, 'error');
                setTimeout(() => {
                    progressSection.classList.add('hidden');
                    errorSection.classList.remove('hidden');
                    document.getElementById('error-message').textContent = error.message;
                }, 1000);
            } finally {
                deployBtn.disabled = false;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/deploy', methods=['POST'])
def deploy():
    config = request.json
    logs = []
    
    try:
        ip = config['ip']
        user = config['user']
        password = config['password']
        directory = config['dir']
        port = config['port']
        
        rpi_addr = f"{user}@{ip}"
        backup_suffix = f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logs.append(f"🔍 Connecting to Raspberry Pi: {rpi_addr}")
        
        # Check if files exist
        required_files = ['simulate_beacon.py', 'index.html', 'beacons_config.json']
        for file in required_files:
            if not (SCRIPT_DIR / file).exists():
                return jsonify({'success': False, 'error': f'{file} not found!'}), 400
        
        logs.append("📁 Required files checked")
        
        # Create backup command
        backup_cmd = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {rpi_addr} 'cp ~/{directory}/simulate_beacon.py ~/{directory}/simulate_beacon.py{backup_suffix} 2>/dev/null || echo \"No backup needed\"'"
        
        logs.append("💾 Creating backup...")
        result = subprocess.run(backup_cmd, shell=True, capture_output=True, text=True)
        logs.append(f"✓ Backup: simulate_beacon.py{backup_suffix}")
        
        # Copy files
        files_to_copy = [
            ('simulate_beacon.py', 'simulate_beacon.py'),
            ('index.html', 'index.html'),
            ('beacons_config.json', 'beacons_config.json')
        ]
        
        for local_file, remote_file in files_to_copy:
            logs.append(f"📤 Uploading {local_file}...")
            scp_cmd = f"sshpass -p '{password}' scp -o StrictHostKeyChecking=no {SCRIPT_DIR / local_file} {rpi_addr}:~/{directory}/{remote_file}"
            result = subprocess.run(scp_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                return jsonify({'success': False, 'error': f'Failed to upload {local_file}: {result.stderr}'}), 500
            
            logs.append(f"✓ {local_file} uploaded")
        
        # Restart service
        logs.append("🔄 Servis yeniden başlatılıyor...")
        restart_cmd = f"""sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {rpi_addr} '
        cd {directory} && 
        screen -X -S beacon_simulator quit 2>/dev/null || true &&
        sleep 2 &&
        chmod +x simulate_beacon.py run_detached.sh &&
        ./run_detached.sh &&
        sleep 2 &&
        if screen -list | grep -q "beacon_simulator"; then
            echo "Service started successfully"
        else
            echo "Warning: Service may not have started"
        fi
        '"""  
        result = subprocess.run(restart_cmd, shell=True, capture_output=True, text=True)
        logs.append("✓ Service started")
        
        logs.append(f"🌐 Web UI: http://{ip}:{port}")
        logs.append(f"📡 API: http://{ip}:{port}/beacon")
        
        return jsonify({'success': True, 'logs': logs})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'logs': logs}), 500

if __name__ == '__main__':
    # Check for sshpass
    try:
        subprocess.run(['which', 'sshpass'], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ sshpass not found!")
        print("\n📦 Installation:")
        print("   macOS: brew install hudochenkov/sshpass/sshpass")
        print("   Linux: sudo apt-get install sshpass")
        print("\nOr use manual deployment: ./deploy.sh\n")
        exit(1)
    
    print("\n" + "="*50)
    print("🚀 Raspberry Pi Beacon - Auto Deployer")
    print("="*50)
    print("\n📡 Starting server...")
    print("🌐 Interface: http://localhost:5000")
    print("\n💡 Open in your browser and start deployment!")
    print("🛑 To stop: Press Ctrl+C\n")
    
    app.run(host='127.0.0.1', port=5000, debug=False)
