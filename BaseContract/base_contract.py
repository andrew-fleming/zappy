import json
import os
from web3 import Web3

infura = 'https://kovan.infura.io/v3/afaba81a13fd484492da91b0baeb10d0'
w3 = Web3(Web3.HTTPProvider(infura))
#print(w3.isConnected())




def load_json(name: str) -> str:
    path = f"{os.path.dirname(os.path.dirname(__file__))}/packages/artifacts/"
    with open(os.path.abspath(path + f"{name}.json")) as f:
        json_file = json.load(f)
    return json_file

def load_abi(name: str) -> dict:
    obj = load_json(name)
    abi = obj['abi']
    return abi

def load_address(name: str, netId: int or str) -> dict:
    a_dict = load_json(name)
    addr = a_dict['networks']
    network_address = addr[netId]['address']
    return network_address




class BaseContract:
    def __init__(
        self,
        provider: any,
        web3: any,
        contract: any,
        networkId: int,
        coordinator: any,
        artifact: any,
        name: str,
        address: str or None
    ) -> None:
        print('foo')



