"""
File: config_loader.py
Author(s): Wai Man Cheng, ChatGPT (OpenAI 4.0 AI Assistant)
Date: 2025-04-09

Description:
------------
Loads test configuration from CLI or prompts with defaults for performance testing.
Designed for manual performance test mode using user-defined or default parameters.

Inputs:
-------
- CLI args (optional)
- Prompts (if CLI not given)
- Defaults fallback

Outputs:
--------
- Dictionary containing all test configuration
"""
import argparse
from utils.test_schemas import TEST_SCHEMAS
import os
import json
import yaml
from datetime import datetime

def load_test_config():
    # Step 1: Parse only --test_type, disable help to avoid conflict
    # parse_known_args(): Parses only known args (in this case --test_type)
    # Leaves the rest (e.g., --ssid, --direction) for later
    base_parser = argparse.ArgumentParser(description="Dynamic test configuration loader", add_help=False)
    base_parser.add_argument("--test_type", required=True, choices=TEST_SCHEMAS.keys(), help="Type of test to run")
    base_parser.add_argument("--mock", action="store_true", help="Run in mock mode without real devices")
    args, remaining_argv = base_parser.parse_known_args()

    test_type = args.test_type
    schema = TEST_SCHEMAS[test_type]

    # Step 2: Now parse schema-specific fields, this parser inherits --test_type from earlier parser
    full_parser = argparse.ArgumentParser(parents=[base_parser])

    for key, default in schema.items():
        full_parser.add_argument(f"--{key}", type=type(default), default=None)

    full_args = full_parser.parse_args()
    config = {"test_type": test_type, "mock": args.mock}

    for key, default in schema.items():
        value = getattr(full_args, key)
        if value is not None:
            config[key] = value
        else:
            prompt = f"{key.replace('_', ' ').title()} [{default}]: "
            input_val = input(prompt)
            config[key] = type(default)(input_val) if input_val else default

    print("\n✅ Final configuration for test:", test_type)
    for k, v in config.items():
        print(f"{k}: {v}")

    save_config_file(config)
    return config

def save_config_file(config, folder="run_logs"):
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_base = f"{config['test_type']}_config_{timestamp}"

    json_path = os.path.join(folder, f"{filename_base}.json")
    yaml_path = os.path.join(folder, f"{filename_base}.yaml")

    # Save JSON
    with open(json_path, "w") as jf:
        json.dump(config, jf, indent=2)

    # Save YAML
    with open(yaml_path, "w") as yf:
        yaml.dump(config, yf)

    print(f"\n📝 Config saved to:\n - {json_path}\n - {yaml_path}")
