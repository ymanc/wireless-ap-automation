# test_stats_runner.py
# Author: Wai Man Cheng & ChatGPT
# Test script for validating stats_runner.py functionality

from datetime import datetime, timedelta
from threading import Event, Thread
from collectors.stats_runner import (
    gather_all_stat_commands,
    run_stats_collection,
    run_during_test_stats
)

# Generate a timestamped folder name
timestamp_dir = datetime.now().strftime("ap_stats_%Y%m%d_%H%M%S")

def simulate_test_duration(stop_event, duration_sec=10):
    import time
    print(f"🕒 Simulating test duration for {duration_sec} seconds...")
    time.sleep(duration_sec)
    stop_event.set()

def run_test():
    print("🔧 Gathering all stat commands (mock mode, prompt only)...")
    gather_all_stat_commands(testbed_path="testbed.yaml", device_name="ap")

    print("\n🚀 Starting BEFORE test stats collection...")
    run_stats_collection(
        phase="before_test",
        testbed_path="testbed.yaml",
        device_name="ap",
        mock=True,
        timestamp_dir=timestamp_dir
    )

    print("\n🚦 Starting DURING test stats collection (will auto-stop)...")
    stop_event = Event()
    stats_thread = Thread(
        target=run_during_test_stats,
        args=(datetime.now(), stop_event),
        kwargs={
            "testbed_path": "testbed.yaml",
            "device_name": "ap",
            "mock": True,
            "timestamp_dir": timestamp_dir
        }
    )
    stats_thread.start()

    simulate_test_duration(stop_event, duration_sec=10)
    stats_thread.join()

    print("\n🧹 Starting AFTER test stats collection...")
    run_stats_collection(
        phase="after_test",
        testbed_path="testbed.yaml",
        device_name="ap",
        mock=True,
        timestamp_dir=timestamp_dir
    )

    print(f"\n✅ Test completed. All stats saved under: run_logs/{timestamp_dir}/")

if __name__ == "__main__":
    run_test()
