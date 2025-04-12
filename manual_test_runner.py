# manual_test_runner.py
# Author(s): Wai Man Cheng, ChatGPT (OpenAI 4.0 AI Assistant)
# Description:
# ------------
# Main script to run tests manually based on user-configured parameters.
# Loads dynamic configuration using the config_loader, then dispatches the selected test case.

from utils.config_loader import load_test_config
from tests.generic_test_runner import run_test

if __name__ == "__main__":
    config = load_test_config()
    run_test(config)
