# test_stats_collector.py
from collectors.stats_collector import collect_stat_block
from datetime import datetime, timedelta

timestamp_dir = datetime.now().strftime("ap_stats_%Y%m%d_%H%M%S")

collect_stat_block(
    name="version",
    testbed_path="testbed.yaml",
    device_name="ap",
    mock=True,
    timestamp_dir=timestamp_dir
)

collect_stat_block(
    name="cpu",
    testbed_path="testbed.yaml",
    device_name="ap",
    mock=True,
    start_time=datetime.now(),
    end_time=datetime.now() + timedelta(minutes=2),
    interval_sec=60,
    timestamp_dir=timestamp_dir
)
