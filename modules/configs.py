import yaml

def load_drone_config(config_path="./configs/drone.yaml"):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config["drone"]

def load_llm_config(config_path="./configs/llm.yaml"):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config["llm"]

def load_command_docs(config_path="./configs/commands.yaml"):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config["commands"]

def load_command_list(config_path="./configs/commands.yaml"):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return [cmd["title"].upper() for cmd in config["commands"]]