# performance_test_runner.py
# Author(s): Wai Man Cheng, ChatGPT (OpenAI 4.0 AI Assistant)
# Description:
# Controls the performance test workflow, including user prompts and stat/log orchestration

import os
import time
import threading
from datetime import datetime

from utils.log_command_manager import get_log_commands
from utils.log_collector import collect_logs_from_testbed
from utils.log_analyzer import run_log_analysis
from collectors.stats_runner import (
    run_stats_collection,
    run_during_test_stats,
    gather_all_stat_commands
)

def run_performance_test(config):
    print("\n🔧 [Performance Test Started]")

    print("🧾 Test Parameters:")
    for key, val in config.items():
        print(f"- {key}: {val}")

    print("\n🔄 Preparing environment...")

    local_epoch = time.time()
    ap_epoch = local_epoch + 2  # simulate AP 2s ahead
    time_offset = ap_epoch - local_epoch
    print(f"📡 Time offset recorded: AP is {round(time_offset, 2)} seconds ahead.")

    device_id = config.get("device_id") or input("Enter device ID/name: ").strip()
    log_commands = get_log_commands(device_id)
    config.update({
        "device_id": device_id,
        "log_commands": log_commands,
        "log_time_offset": time_offset
    })

    # Step 1: Gather all stat commands up front
    gather_all_stat_commands(testbed_path="testbed.yaml", device_name=device_id)

    # Step 2: Run pre-test stat collection
    run_stats_collection("before_test", testbed_path="testbed.yaml", device_name=device_id, mock=config.get("mock", False))

    input("\n📥 Press ENTER to start the test. Please connect the client and start traffic.")
    start_time = datetime.now()

    # Step 3: Start background stats collection during the test
    stop_event = threading.Event()
    stats_thread = threading.Thread(
        target=run_during_test_stats,
        kwargs={
            "start_time": start_time,
            "stop_event": stop_event,
            "testbed_path": "testbed.yaml",
            "device_name": device_id,
            "mock": config.get("mock", False)
        },
        daemon=True
    )
    stats_thread.start()

    # Step 4: Wait for user to stop test
    user_input = input("📤 Press ENTER to stop the test once traffic ends (or type 'q' to terminate without collecting stats/logs): ")
    end_time = datetime.now()

    if user_input.strip().lower() == 'q':
        print("❌ Test manually terminated by user. Skipping stats and log collection.")
        stop_event.set()
        stats_thread.join()
        return

    stop_event.set()
    stats_thread.join()

    # Step 5: Run post-test stats
    run_stats_collection("after_test", testbed_path="testbed.yaml", device_name=device_id, mock=config.get("mock", False))

    # Step 6: Log collection and analysis
    print("\n📥 Collecting post-test logs...")
    log_dir = collect_logs_from_testbed(
        testbed_path="testbed.yaml",
        device_name=device_id,
        commands=config["log_commands"],
        mock=config.get("mock", False),
        start_time=start_time,
        end_time=end_time
    )

    print("\n🧐 Analyzing collected logs...")
    run_log_analysis(log_dir)

    print("\n✅ [Performance Test Completed]")
