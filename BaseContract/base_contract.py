import json
import os
from web3 import Web3

# Replacing Utils and artifactDir in monorepo
#
# Helper function for load_abi and load_address.
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
    try:
        a_dict = load_json(name)
        addr = a_dict['networks']
        network_address = addr[netId]['address']
        return network_address
    except Exception as e:
        print('Error with: ' + str(e))



class BaseContract:
    def __init__(self, artifact_name, network_id, network_provider, coordinator, address, web3):
        self.name = artifact_name
        try:
            self.artifact = artifact_name
            self.network_id = network_id or 1
            coor_artifact_abi = load_abi('ZapCoordinator')
            coor_artifact_address = load_address('ZapCoordinator', self.network_id)
            self.provider = web3 or Web3(network_provider) or Web3(Web3.HTTPProvider('https://cloudflare-eth.com'))
            self.coordinator = self.provider.eth.Contract(coor_artifact_abi, coordinator or coor_artifact_address)
            self.contract = None
            if address:
                self.address = address
            else:
                self.address = self.artifact.networks[self.network_id].address
                if coordinator:
                    self.coordinator.getContract()
                else:
                    self.coordinator = self.provider.eth.Contract(self.artifact.abi, self.address)
        except Exception as e:
            raise e

