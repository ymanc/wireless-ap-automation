# log_generator.py
# Author(s): Wai Man Cheng, ChatGPT (OpenAI 4.0 AI Assistant)
# Description:
# -------------
# Generates mock syslog-style logs with realistic timestamps between a test's
# start and end time. Categories include kernel crash and interface bounce.

import os
import random
from datetime import datetime, timedelta

def generate_mock_logs(output_dir, commands, start_time=None, end_time=None):
    """
    Generates dummy logs with timestamps between start_time and end_time.
    Saves logs per command to files in output_dir.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not start_time:
        start_time = datetime.now()
    if not end_time:
        end_time = start_time + timedelta(seconds=60)

    # Correlated log templates by root cause
    log_templates = {
        "kernel_crash": [
            "ap-kernel: Kernel panic - not syncing: Fatal exception",
            "ap-interface: wlan0 (2.4G) changed state to down",
            "ap-interface: wlan0 (2.4G) changed state to up",
            "ap-interface: wlan1 (5G) changed state to down",
            "ap-interface: wlan1 (5G) changed state to up"
        ],
        "hostapd_crash": [
            "ap-daemon: Process 'hostapd' crashed due to signal 11",
            "ap-interface: wlan0 (2.4G) changed state to down",
            "ap-interface: wlan1 (5G) changed state to down",
            "ap-interface: wlan2 (6G) changed state to down",
            "ap-driver: Restarting wireless driver stack"
        ],
        "memory_cpu_issue": [
            "ap-memory: High memory usage detected: 95%",
            "ap-cpu: CPU core 0 usage: 98%",
            "ap-cpu: CPU core 1 usage: 92%",
            "ap-interface: eth0 changed state to down",
            "ap-interface: eth0 changed state to up"
        ]
    }

    # Flatten all log lines
    all_messages = []
    for group in log_templates.values():
        all_messages.extend(group)

    total_lines = 20
    duration_sec = int((end_time - start_time).total_seconds())

    for i, cmd in enumerate(commands):
        safe_cmd = cmd.replace(" ", "_").replace("/", "_").replace("|", "_")[:30]
        filename = os.path.join(output_dir, f"log_{i+1}_{safe_cmd}.txt")
        lines = []

        for _ in range(total_lines):
            rand_offset = random.randint(0, duration_sec)
            log_time = (start_time + timedelta(seconds=rand_offset)).strftime("%b %d %H:%M:%S")
            message = random.choice(all_messages)
            lines.append(f"{log_time} {message}")

        with open(filename, 'w') as f:
            f.write("\n".join(lines))

        print(f"✅ [MOCK] Saved generated log to {filename}")

# Run standalone
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", help="Directory to write simulated log files")
    parser.add_argument("--duration", type=int, default=60, help="Duration of test in seconds")
    parser.add_argument("--commands", nargs='+', default=["show logging"], help="Command list to simulate")
    args = parser.parse_args()

    start = datetime.now()
    end = start + timedelta(seconds=args.duration)

    generate_mock_logs(args.output_dir, args.commands, start, end)
