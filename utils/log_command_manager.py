# log_command_manager.py
# Author(s): Wai Man Cheng, ChatGPT (OpenAI 4.0 AI Assistant)
# Description:
# -------------
# Utility to manage vendor-specific logging commands for collecting AP logs.
# Loads existing commands, allows user to confirm, edit, add, or delete commands.
# Commands are saved into log_command_registry.yaml

import yaml
import os

REGISTRY_FILE = "utils/log_command_registry.yaml"


def load_registry():
    if not os.path.exists(REGISTRY_FILE):
        return {}
    with open(REGISTRY_FILE, 'r') as file:
        return yaml.safe_load(file) or {}


def save_registry(registry):
    os.makedirs(os.path.dirname(REGISTRY_FILE), exist_ok=True)
    with open(REGISTRY_FILE, 'w') as file:
        yaml.safe_dump(registry, file)


def get_log_commands(device_id):
    registry = load_registry()

    if device_id in registry:
        print(f"📘 Found saved log commands for {device_id}:")
        for i, cmd in enumerate(registry[device_id]['commands']):
            print(f"  {i+1}. {cmd}")
        choice = input("Do you want to (K)eep, (E)dit, or (D)elete these commands? [K/e/d]: ").strip().lower()
        if choice == 'k' or choice == '':
            return registry[device_id]['commands']
        elif choice == 'd':
            del registry[device_id]
            save_registry(registry)
        elif choice == 'e':
            print("✏️  Editing log commands...")

    # Create new or edit mode
    print(f"➕ Enter up to 3 log commands for {device_id} (press enter to skip):")
    commands = []
    for i in range(3):
        cmd = input(f"Command {i+1}: ").strip()
        if cmd:
            commands.append(cmd)
    
    if commands:
        registry[device_id] = {"commands": commands}
        save_registry(registry)
        print(f"✅ Commands saved for {device_id}.")
        return commands
    else:
        print("⚠️ No commands entered. Proceeding without log collection.")
        return []


# Example usage for testing
if __name__ == "__main__":
    device_id = input("Enter device ID/name: ").strip()
    log_cmds = get_log_commands(device_id)
    print("Final log command list:", log_cmds)
