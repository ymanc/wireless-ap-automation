# stats_generator.py
# Author(s): Wai Man Cheng, ChatGPT (OpenAI 4.0 AI Assistant)
# Description:
# -------------
# Generates mock stats for AP version, performance, CPU usage, and memory usage
# for testing without live SSH access (mock mode)

import os
import random
import time
from datetime import datetime, timedelta


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # resolves to collectors/
SAMPLE_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "mock_samples"))  # resolves to root

#SAMPLE_DIR = "mock_samples"

def _load_sample(file_name):
    path = os.path.join(SAMPLE_DIR, file_name)
    print(f"Loading sample file: {path}")
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return f"[MOCK] Sample file '{file_name}' not found."
    with open(path, 'r') as f:
        return f.read()

def generate_ap_version_stats(output_dir):
    print("generate ap version")
    content = _load_sample("version.txt")
    output_path = os.path.join(output_dir, "version.txt")
    with open(output_path, 'w') as f:
        f.write(content)
    print(f"📄 [MOCK] Saved AP version stats to {output_path}")
    return output_path

def generate_performance_stats(output_dir):
    content = _load_sample("perstats.txt")
    output_path = os.path.join(output_dir, "performance_stats.txt")
    with open(output_path, 'w') as f:
        f.write(content)
    print(f"📄 [MOCK] Saved performance stats to {output_path}")
    return output_path

def generate_cpu_stats(output_dir, start_time, end_time, interval_sec=60):
    output_path = os.path.join(output_dir, "cpu_usage.csv")
    with open(output_path, 'w') as f:
        f.write("timestamp,cpu_0,cpu_1,cpu_2,cpu_3\n")
        current = start_time
        while current <= end_time:
            timestamp = current.strftime("%Y-%m-%d %H:%M:%S")
            values = [random.randint(70, 100) for _ in range(4)]
            f.write(f"{timestamp},{values[0]},{values[1]},{values[2]},{values[3]}\n")
            current += timedelta(seconds=interval_sec)
    print(f"📄 [MOCK] Saved CPU usage stats to {output_path}")
    return output_path

def generate_memory_stats(output_dir, start_time, end_time, interval_sec=60):
    output_path = os.path.join(output_dir, "memory_usage.csv")
    with open(output_path, 'w') as f:
        f.write("timestamp,free_mb,available_mb\n")
        current = start_time
        while current <= end_time:
            timestamp = current.strftime("%Y-%m-%d %H:%M:%S")
            free = random.randint(300, 500)
            available = free + random.randint(100, 300)
            f.write(f"{timestamp},{free},{available}\n")
            current += timedelta(seconds=interval_sec)
    print(f"📄 [MOCK] Saved memory usage stats to {output_path}")
    return output_path

def generate_clear_stats(output_dir):
    content = _load_sample("clearcounters.txt")
    output_path = os.path.join(output_dir, "clear_stats.txt")
    with open(output_path, 'w') as f:
        f.write(content)
    print(f"📄 [MOCK] Saved clear stats to {output_path}")
    return output_path

if __name__ == "__main__":
    from datetime import datetime, timedelta

    # Create dummy output directory
    test_output_dir = "run_logs/debug_stats"
    os.makedirs(test_output_dir, exist_ok=True)

    start = datetime.now()
    end = start + timedelta(minutes=2)

    generate_ap_version_stats(test_output_dir)
    generate_performance_stats(test_output_dir)
    generate_clear_stats(test_output_dir)
    generate_cpu_stats(test_output_dir, start, end, interval_sec=60)
    generate_memory_stats(test_output_dir, start, end, interval_sec=60)
