# stats_runner.py
# Author(s): Wai Man Cheng, ChatGPT (OpenAI 4.0 AI Assistant)
# Description:
# High-level module to orchestrate AP stats collection (version, performance, cpu, memory, etc.)
# Reads schema, determines when/what to collect, and delegates to stats_collector.py

import time
from datetime import datetime, timedelta
import yaml
from threading import Event
from collectors.stats_collector import collect_stat_block

STATS_SCHEMA_PATH = "configs/stats_schema.yaml"

def load_stats_schema():
    with open(STATS_SCHEMA_PATH, 'r') as f:
        return yaml.safe_load(f)

def gather_all_stat_commands(testbed_path="testbed.yaml", device_name="ap"):
    schema = load_stats_schema()
    for stat_name, config in schema.items():
        collection = config.get("collection", {})
        if (
            collection.get("before_test", False)
            or collection.get("after_test", False)
            or collection.get("during_test", {}).get("enabled", False)
        ):
            print(f"📘 Prompting for stat: {stat_name}")
            collect_stat_block(
                name=stat_name,
                testbed_path=testbed_path,
                device_name=device_name,
                mock=False,
                prompt_only=True
            )

def run_stats_collection(phase, testbed_path="testbed.yaml", device_name="ap", mock=False, timestamp_dir=None):
    schema = load_stats_schema()
    collected_files = []

    print(f"\n📊 Running '{phase}' stats collection...")
    for stat_name, config in schema.items():
        collection = config.get("collection", {})
        if collection.get(phase, False):
            result_file = collect_stat_block(
                name=stat_name,
                testbed_path=testbed_path,
                device_name=device_name,
                mock=mock,
                timestamp_dir=timestamp_dir
            )
            if result_file:
                collected_files.append(result_file)
    return collected_files

def run_during_test_stats(start_time, stop_event: Event, testbed_path="testbed.yaml", device_name="ap", mock=False, timestamp_dir=None):
    schema = load_stats_schema()
    print(f"\n📈 Starting 'during_test' stats from {start_time}...")

    next_run_time = {
        name: start_time
        for name, cfg in schema.items()
        if cfg.get("collection", {}).get("during_test", {}).get("enabled", False)
    }

    while not stop_event.is_set():
        now = datetime.now()
        for stat_name, config in schema.items():
            during_cfg = config.get("collection", {}).get("during_test", {})
            if not during_cfg.get("enabled", False):
                continue

            interval = during_cfg.get("interval_sec", 60)
            if now >= next_run_time[stat_name]:
                collect_stat_block(
                    name=stat_name,
                    testbed_path=testbed_path,
                    device_name=device_name,
                    mock=mock,
                    start_time=start_time,
                    end_time=now,
                    interval_sec=interval,
                    timestamp_dir=timestamp_dir
                )
                next_run_time[stat_name] = now + timedelta(seconds=interval)

        stop_event.wait(timeout=1)

    print("✅ Completed 'during_test' periodic stats collection.")

if __name__ == "__main__":
    from datetime import datetime, timedelta
    from threading import Event

    ts_dir = datetime.now().strftime("ap_stats_%Y%m%d_%H%M%S")

    run_stats_collection(
        phase="before_test",
        testbed_path="testbed.yaml",
        device_name="ap",
        mock=True,
        timestamp_dir=ts_dir
    )

    start = datetime.now()
    stop_event = Event()
    end = start + timedelta(minutes=2)
    run_during_test_stats(
        start_time=start,
        stop_event=stop_event,
        testbed_path="testbed.yaml",
        device_name="ap",
        mock=True,
        timestamp_dir=ts_dir
    )

    run_stats_collection(
        phase="after_test",
        testbed_path="testbed.yaml",
        device_name="ap",
        mock=True,
        timestamp_dir=ts_dir
    )
