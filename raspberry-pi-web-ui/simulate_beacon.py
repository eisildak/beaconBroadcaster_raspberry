#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BACKWARD COMPATIBLE UPDATE - All existing APIs work as before

import argparse
import time
import subprocess
import json
import os
from flask import Flask, jsonify, request, send_file
from pathlib import Path

# Config file path (NEW - doesn't affect existing functionality)
SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / 'beacons_config.json'

def load_beacons_config():
	"""Load beacons configuration from JSON file (NEW)"""
	try:
		if CONFIG_FILE.exists():
			with open(CONFIG_FILE, 'r') as f:
				return json.load(f)
	except:
		pass
	return []

def save_beacons_config(beacons):
	"""Save beacons configuration to JSON file (NEW)"""
	try:
		with open(CONFIG_FILE, 'w') as f:
			json.dump(beacons, f, indent=2)
	except Exception as e:
		print(f"Failed to save config: {e}")

def hexstring_to_bytes_with_spaces(hex_string):
	arr = []
	for i in range(0, len(hex_string), 2):
		arr.append(hex_string[i] + hex_string[i+1])
	return ' '.join(arr)
   		   
def get_ibeacon_payload(uuid,major,minor, rssi):
	adv_hex = uuid.replace('-', '')+major.to_bytes(2, byteorder='big').hex()+minor.to_bytes(2, byteorder='big').hex()
	adv_bytes_hex = hexstring_to_bytes_with_spaces(adv_hex)
	rssi_byte = (256 + rssi if rssi < 0 else rssi).to_bytes(1, byteorder='big', signed=False).hex()
	ibeacon_payload = f"1E 02 01 06 1A FF 4C 00 02 15 {adv_bytes_hex} {rssi_byte}"
	return ibeacon_payload	

current_beacon = None
def start_ibeacon(uuid, major, minor, rssi=-59, min_interval=100, max_interval=100, interface='hci0'):
	try:
		restart_ble(interface)
		set_ibeacon_advertisment(uuid, major, minor, rssi, interface)
		set_advertisment_interval(min_interval, max_interval, interface)
		return True
	except subprocess.CalledProcessError as e:
		print(f"Failed to start iBeacon advertising: {e}")
	return False

multiplex_running = False
multiplex_beacons = None
def start_multiplex_ibeacons(beacons, interface='hci0'):
	global multiplex_running, multiplex_beacons
	multiplex_running = True
	multiplex_beacons = beacons
	i = 0
	while multiplex_running:
		j = i % len(beacons)
		beacon = beacons[j]
		start_ibeacon(beacon["uuid"], beacon["major"], beacon["minor"], beacon.get("rssi", -69), 100, 100, interface)
		time.sleep(4*100/1000)
		i += 1

def stop_advertisement(interface='hci0'):
	global multiplex_running, current_beacon, multiplex_beacons
	multiplex_running = False
	current_beacon = None
	multiplex_beacons = None
	time.sleep(1)
	subprocess.run(['sudo', 'hciconfig', interface, 'down'], check=False)

def set_advertisment_interval(min_interval, max_interval, interface='hci0'):
	min_interval_le = int(min_interval * 1.6).to_bytes(2, byteorder='little').hex()
	max_interval_le = int(max_interval * 1.6).to_bytes(2, byteorder='little').hex()
	subprocess.run((f'sudo hcitool -i {interface} cmd 0x08 0x0006 '+hexstring_to_bytes_with_spaces(min_interval_le)+' '+hexstring_to_bytes_with_spaces(max_interval_le)+' 03 00 00 00 00 00 00 00 00 07 00').split(), check=True)
	subprocess.run(f'sudo hcitool -i {interface} cmd 0x08 0x000a 01'.split(), check=True)
	
def set_ibeacon_advertisment(uuid, major, minor, rssi=-59, interface='hci0'):
	global current_beacon
	current_beacon = {'uuid': uuid, 'major': major, 'minor': minor, 'rssi': rssi, 'date': time.time()}
	ibeacon_payload = get_ibeacon_payload(uuid, major, minor, rssi)
	subprocess.run((f'sudo hcitool -i {interface} cmd 0x08 0x0008 '+ibeacon_payload).split(), check=True)
			
	
def restart_ble(interface='hci0'):
	subprocess.run(f'sudo hciconfig {interface} down'.split(), check=False)
	subprocess.run(f'sudo hciconfig {interface} up'.split(), check=False)
	
def power_on_usb(port_number=2, location='1-1'):
	subprocess.run(f"sudo uhubctl -l {location} -p {port_number} -a 1".split(), check=False)
	
def power_off_usb(port_number=2, location='1-1'):
	subprocess.run(f"sudo uhubctl -l {location} -p {port_number} -a 0".split(), check=False)

def get_usb_power(port_number=2, location='1-1'):
	try:
		result = subprocess.run(f"sudo uhubctl -l {location} -p {port_number}".split(), capture_output=True, text=True, check=True)
		output = result.stdout
		lines = output.split('\n')
		for line in lines:
		    if f"Port {port_number}:" in line:
		        if "power" in line:
		            return True
		        else:
		            return False
		return False
	except subprocess.CalledProcessError as e:
		print(f"Failed to run command: {e}")
	return False
                    
def start_api(args):
	app = Flask(__name__, static_folder='.')

	# ═══════════════════════════════════════════════════════════
	# EXISTING ENDPOINTS - DO NOT MODIFY (for Appium compatibility)
	# ═══════════════════════════════════════════════════════════
	
	@app.route('/beacon/enable/<uuid>/<int:major>/<int:minor>', methods=['GET'])
	def enable_beacon(uuid, major, minor):
		"""EXISTING: Enable beacon (Appium-compatible)"""
		rssi = int(request.args.get('rssi', args.rssi))
		success = start_ibeacon(uuid, major, minor, rssi, args.interval, args.interval, args.bluetooth_interface)
		if success:
			print(f"✅ Beacon enabled: {uuid} (Major: {major}, Minor: {minor}, RSSI: {rssi})")
			return jsonify({'status': 'enabled', 'uuid': uuid, 'major': major, 'minor': minor, 'rssi': rssi}), 200
		else:
			print(f"❌ Failed to enable beacon: {uuid}")
			return jsonify({'error': 'Failed to start beacon broadcasting'}), 500
		
	@app.route('/beacon/disable', methods=['GET'])
	def disable_beacon():
		"""EXISTING: Disable beacon (Appium-compatible)"""
		print("🛑 Stopping beacon...")
		stop_advertisement(args.bluetooth_interface)
		print("✅ Beacon stopped")
		return jsonify({'status': 'disabled'}), 200
	
	@app.route('/beacon', methods=['GET'])
	def get_beacon():
		"""EXISTING: Get current beacon (Appium-compatible)"""
		global multiplex_beacons, current_beacon, multiplex_running
		beacons = multiplex_beacons if multiplex_running else ([current_beacon] if current_beacon else [])
		return jsonify(beacons), 200
		
	@app.route('/beacon/usb/disable', methods=['GET'])
	def disable_usb_beacon():
		"""EXISTING: Disable USB (Appium-compatible)"""
		power_off_usb(args.usb_port, args.usb_location)
		return get_usb_beacon_status()
	
	@app.route('/beacon/usb/enable', methods=['GET'])
	def enable_usb_beacon():
		"""EXISTING: Enable USB (Appium-compatible)"""
		power_on_usb(args.usb_port, args.usb_location)
		return get_usb_beacon_status()

	@app.route('/beacon/usb', methods=['GET'])
	def get_usb_beacon_status():
		"""EXISTING: Get USB status (Appium-compatible)"""
		is_on = get_usb_power(args.usb_port, args.usb_location)
		return jsonify({'power': is_on}), 200

	# ═══════════════════════════════════════════════════════════
	# NEW ENDPOINTS - Web UI support (doesn't break existing APIs)
	# ═══════════════════════════════════════════════════════════

	@app.route('/', methods=['GET'])
	def index():
		"""NEW: Serve web UI (optional - doesn't affect existing API)"""
		try:
			return send_file('index.html')
		except:
			return jsonify({"message": "Web UI not installed. API is working."}), 200

	@app.route('/beacon/list', methods=['GET'])
	def list_beacons():
		"""NEW: Get saved beacons (optional - for web UI)"""
		beacons = load_beacons_config()
		return jsonify(beacons), 200

	@app.route('/beacon/add', methods=['POST'])
	def add_beacon():
		"""NEW: Add beacon to config (optional - for web UI)"""
		try:
			beacon = request.json
			beacons = load_beacons_config()
			beacons.append(beacon)
			save_beacons_config(beacons)
			return jsonify(beacons), 200
		except Exception as e:
			return jsonify({"error": str(e)}), 500

	@app.route('/beacon/delete/<int:index>', methods=['DELETE'])
	def delete_beacon(index):
		"""NEW: Delete beacon from config (optional - for web UI)"""
		try:
			beacons = load_beacons_config()
			if 0 <= index < len(beacons):
				beacons.pop(index)
				save_beacons_config(beacons)
			return jsonify(beacons), 200
		except Exception as e:
			return jsonify({"error": str(e)}), 500
	
	# Initialize
	print("🚀 Beacon Broadcaster API Starting...")
	print(f"📡 API Endpoint: http://0.0.0.0:{args.port}")
	print(f"🌐 Web UI: http://0.0.0.0:{args.port}/ (if index.html exists)")
	print(f"🔧 Bluetooth Interface: {args.bluetooth_interface}")
	print("")
	print("✅ All existing Appium endpoints active:")
	print(f"   GET  /beacon/enable/<uuid>/<major>/<minor>")
	print(f"   GET  /beacon/disable")
	print(f"   GET  /beacon")
	print("")
	
	stop_advertisement(args.bluetooth_interface)
	app.run(port=args.port, host='0.0.0.0', debug=False)
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Simulate ibeacon')
	parser.add_argument('--uuid', '-u', type=str, default='bbbbbbbb-aaaa-dddd-beef-0000000000fe', help='UUID of the ibeacon')
	parser.add_argument('--major', '-M', type=int, default=1, help='major of the beacon [0-65535]')
	parser.add_argument('--minor', '-m', type=int, default=2, help='minor of the beacon [0-65535]')
	parser.add_argument('--interval', '-i', type=int, default=100, help='advertisment interval in ms')
	parser.add_argument('--rssi', '-r', type=int, default=-59, help='RSSI in dbm at 1 meter')
	parser.add_argument('--port', '-p', type=int, default=-1, help='Port to listen on')
	parser.add_argument('--usb-port', '-P', type=int, default=2, help='USB port to control')
	parser.add_argument('--usb-location', '-L', type=str, default='1-1', help='USB port location to control')
	parser.add_argument('--bluetooth-interface', '-I', type=str, default='hci0', help='Bluetooth interface to control')

	args = parser.parse_args()
	if args.port <= 0:
		start_ibeacon(args.uuid, args.major, args.minor, args.rssi, args.interval, args.interval, args.bluetooth_interface)
	else:
		start_api(args)
