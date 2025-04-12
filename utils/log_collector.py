# log_collector.py
# Author(s): Wai Man Cheng, ChatGPT (OpenAI 4.0 AI Assistant)
# Description:
# -------------
# Collects logs from an AP using pyATS-based SSH session defined in testbed.yaml.
# Executes user-defined log commands and saves outputs for post-test analysis.

import os
import socket
from datetime import datetime
from genie.testbed import load
from time import time
from utils.log_generator import generate_mock_logs


def is_port_open(ip, port=22, timeout=5):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except Exception:
        return False

def collect_logs_from_testbed(testbed_path, device_name, commands, mock=False, start_time=None, end_time=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = f"run_logs/logs_{device_name}_{timestamp}"
    os.makedirs(log_dir, exist_ok=True)

    try:
        testbed = load(testbed_path)
        device = testbed.devices[device_name]
        ip = device.connections.get("ssh", {}).get("ip", "")

        if mock and not is_port_open(ip, timeout=5):
            print(f"⚠️ [MOCK MODE] SSH port {ip}:22 unreachable. Skipping real connect.")
            raise Exception("Mock mode SSH check failed")

        print(f"🔌 Attempting SSH connection to device: {device_name} ...")
        device.connect(log_stdout=False, learn_hostname=True)
        print(f"✅ Connected successfully.")

        for i, cmd in enumerate(commands):
            print(f"▶️ Running: {cmd}")
            try:
                output = device.execute(cmd)
            except Exception as e:
                output = f"[ERROR] Failed to run '{cmd}': {str(e)}"

            safe_cmd = cmd.replace(" ", "_").replace("/", "_").replace("|", "_")[:30]
            filename = os.path.join(log_dir, f"log_{i+1}_{safe_cmd}.txt")

            with open(filename, 'w') as f:
                f.write(output)
            print(f"✅ Saved output to {filename}")

        device.disconnect()
        print("📁 All logs saved.")

    except Exception as e:
        if mock:
            print(f"⚠️ [MOCK MODE] SSH connection to {device_name} bypassed due to: {str(e)}")
            print("🔁 Generating simulated log outputs...")
            generate_mock_logs(log_dir, commands, start_time=start_time, end_time=end_time)
            print("📁 [MOCK] All simulated logs saved.")
        else:
            print(f"❌ [ERROR] SSH connection failed to {device_name}: {str(e)}")
            print("🛑 Terminating log collection.")

    return log_dir

# Example usage
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true", help="Run in mock mode without real AP")
    args = parser.parse_args()

    yaml_path = "testbed.yaml"
    ap_name = "ap"
    log_cmds = [
        "terminal monitor",
        "show logging | include ERROR",
        "show platform crash"
    ]
    collect_logs_from_testbed(yaml_path, ap_name, log_cmds, mock=args.mock)
