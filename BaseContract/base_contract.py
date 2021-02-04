import json
import os

def _load_abi(name: str) -> str:
    path = f"{os.path.dirname(os.path.dirname(__file__))}\packages\\artifacts/"
    with open(os.path.abspath(path + f"{name}.json")) as f:
        json_file = json.load(f)
        abi = json_file['abi']
    return abi

