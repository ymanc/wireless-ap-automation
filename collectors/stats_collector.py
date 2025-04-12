# stats_collector.py
# Author(s): Wai Man Cheng, ChatGPT (OpenAI 4.0 AI Assistant)
# Description:
# Generalized AP stats collector using schema-driven configuration
# Supports real or mock collection and persistent command management

import os
import socket
import yaml
from datetime import datetime
from genie.testbed import load
from collectors.stats_generator import (
    generate_ap_version_stats,
    generate_performance_stats,
    generate_cpu_stats,
    generate_memory_stats,
    generate_clear_stats
)

# Global cache to prevent reloading commands more than once
STAT_COMMAND_CACHE = {}

def load_stat_schema(stat_name, schema_path="configs/stats_schema.yaml"):
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"❌ Stat schema file not found: {schema_path}")
    with open(schema_path, 'r') as f:
        schema = yaml.safe_load(f)
    return schema.get(stat_name, {})

def is_port_open(ip, port=22, timeout=5):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except Exception:
        return False

def load_stat_commands(name, device_name, num_cmds, registry_file="collectors/stats_command_registry.yaml"):
    existing_cmds = {}
    if os.path.exists(registry_file):
        with open(registry_file, 'r') as f:
            existing_cmds = yaml.safe_load(f) or {}

    key = f"{device_name}_{name}"
    if key in existing_cmds and existing_cmds[key]:
        print(f"\n📘 Found saved {name} command(s) for {device_name}:")
        for i, cmd in enumerate(existing_cmds[key], 1):
            print(f"  {i}. {cmd}")
        choice = input("Do you want to (K)eep, (E)dit, or (D)elete these commands? [K/e/d]: ").strip().lower()
        if choice == 'k' or choice == '':
            return existing_cmds[key]
        elif choice == 'd':
            del existing_cmds[key]

    new_cmds = []
    for i in range(num_cmds):
        cmd = input(f"Enter command {i+1} for {name} stats (or leave blank to skip): ").strip()
        if cmd:
            new_cmds.append(cmd)

    if new_cmds:
        existing_cmds[key] = new_cmds
        with open(registry_file, 'w') as f:
            yaml.safe_dump(existing_cmds, f)
    return new_cmds

def collect_stat_block(name, testbed_path="testbed.yaml", device_name="ap", mock=False,
                       start_time=None, end_time=None, interval_sec=60, prompt_only=False,
                       timestamp_dir=None):
    schema = load_stat_schema(name)
    num_cmds = schema.get("cmd_num", 1)
    if prompt_only:
        load_stat_commands(name, device_name, num_cmds)
        return None

    print(f"\n🔍 Collecting AP {name} stats (Mock: {mock})")
    #cmds = load_stat_commands(name, device_name, num_cmds)
    key = f"{device_name}_{name}"
    if key not in STAT_COMMAND_CACHE:
        cmds = load_stat_commands(name, device_name, num_cmds)
        STAT_COMMAND_CACHE[key] = cmds
    else:
        cmds = STAT_COMMAND_CACHE[key]
    if not cmds:
        print("⚠️ No commands provided. Skipping.")
        return None

    try:
        tb = load(testbed_path)
        device = tb.devices[device_name]
    except Exception as e:
        print(f"❌ Failed to load testbed or device '{device_name}': {e}")
        return None

    ip = device.connections.get("cli", {}).get("ip")
    if not mock and ip and not is_port_open(ip):
        print(f"⚠️ SSH port not reachable on {ip}. Switching to MOCK mode.")
        mock = True

    folder = timestamp_dir or "ap_stats"
    save_dir = os.path.join("run_logs", folder, name)
    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(save_dir, f"{name}_stats_{timestamp}.txt")

    if mock:
        print(f"⚠️ MOCK mode enabled. Generating mock {name} output...")
        if name == "version":
            return generate_ap_version_stats(save_dir)
        elif name == "performance":
            return generate_performance_stats(save_dir)
        elif name == "cpu":
            if start_time and end_time and interval_sec:
                return generate_cpu_stats(save_dir, start_time, end_time, interval_sec)
            else:
                snapshot_file = os.path.join(save_dir, f"cpu_snapshot_{timestamp}.txt")
                with open(snapshot_file, "w") as f:
                    f.write("[MOCK] Static CPU snapshot (before/after phase)\n")
                print(f"📄 [MOCK] Saved CPU snapshot to {snapshot_file}")
                return snapshot_file
        elif name == "memory":
            if start_time and end_time and interval_sec:
                return generate_memory_stats(save_dir, start_time, end_time, interval_sec)
            else:
                snapshot_file = os.path.join(save_dir, f"memory_snapshot_{timestamp}.txt")
                with open(snapshot_file, "w") as f:
                    f.write("[MOCK] Static Memory snapshot (before/after phase)\n")
                print(f"📄 [MOCK] Saved Memory snapshot to {snapshot_file}")
                return snapshot_file
        elif name == "clear":
            return generate_clear_stats(save_dir)
        else:
            with open(filename, "w") as f:
                f.write(f"[MOCK OUTPUT] {name}\n")
            return filename
    else:
        try:
            device.connect(log_stdout=False)
            print(f"✅ Connected to {device_name}. Running {name} command(s)...")
            output = "\n\n".join([f"# {cmd}\n" + device.execute(cmd) for cmd in cmds])
        except Exception as e:
            print(f"❌ Error connecting or executing on device: {e}")
            return None

    with open(filename, "w") as f:
        f.write(f"# Timestamp: {timestamp}\n\n{output}\n")

    print(f"📄 Saved {name} stats to {filename}")
    return filename

if __name__ == "__main__":
    from datetime import datetime, timedelta

    collect_stat_block(
        name="version",
        testbed_path="testbed.yaml",
        device_name="ap",
        mock=True,
        timestamp_dir="ap_stats_debug"
    )

    collect_stat_block(
        name="cpu",
        testbed_path="testbed.yaml",
        device_name="ap",
        mock=True,
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(minutes=2),
        interval_sec=60,
        timestamp_dir="ap_stats_debug"
    )
