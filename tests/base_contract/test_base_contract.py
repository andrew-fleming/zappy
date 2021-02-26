import pytest
from web3 import Web3
from BaseContract.base_contract import BaseContract
from BaseContract.utils import Utils    # For monkeypatch
from Artifacts.src.index import Artifacts   # For monkeypatch
from unittest.mock import MagicMock
import asyncio
from unittest.mock import AsyncMock

@pytest.fixture(scope='module')
def default_web3():
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    return w3

@pytest.fixture(scope='module')
def arbitrary_address():
    address = '0x131e22ae3e90f0eeb1fb739eaa62ea0290c3fbe1'
    return address


class TestInstantiation:

    """
    # Sanity check.
    """
    def test_construction(self):
        assert BaseContract

    @pytest.mark.parametrize('artifact_name', ['ARBITER', 'BONDAGE', 'DISPATCH', 'REGISTRY', 'CurrentCost',
                                               'ZAP_TOKEN', 'ZAPCOORDINATOR', 'TOKENDOTFACTORY'])
    def test_instances_of_name_and_artifact(self, arbitrary_address, artifact_name):
        instance = BaseContract(artifact_name=artifact_name)

        assert type(instance.artifact) == dict

        assert instance.name == artifact_name
        assert type(instance.name) == str

        with pytest.raises(AssertionError):
            assert type(instance.artifact) != dict

            assert type(instance.name) != str
            assert instance.name != artifact_name

    """
    #   @notice: The following functions mock the get_artifacts and open_artifacts functions to allow instantiation. 
    #       The get_artifacts and open_artifacts functions are located in BaseContract/src/utils.
    """

    def mock_get_artifacts(self, directory):
        return {'ex_1.json', 'ex_2.json', 'ex_3.json', 'ex_4.json'}

    def mock_open_artifacts(self):
        return '{"Arbiter": {"abi": [], "networks": {"1": {"address": "0x131e22ae3e90f0eeb1fb739eaa62ea0290c3fbe1"}}}}'

    @pytest.mark.skip(reason="My monkeypatches aren't working. Dependencies still getting called.")
#    @pytest.mark.parametrize('artifact_name', ['ARBITER', 'BONDAGE', 'DISPATCH', 'REGISTRY', 'CurrentCost',
#                                               'ZAP_TOKEN', 'ZAPCOORDINATOR', 'TOKENDOTFACTORY'])
    def test_artifacts_directory(self, default_web3, arbitrary_address, monkeypatch):
        #monkeypatch.setattr(Artifacts, 'artifacts', self.mock_open_artifacts)
        #monkeypatch.setattr(Utils, 'open_artifact_in_dir', self.mock_open_artifacts)
        #monkeypatch.setattr(Utils, 'get_artifacts', self.mock_get_artifacts)
        instance = BaseContract(artifact_name='ARBITER', artifacts_dir='Artifacts/contract/')
        assert instance.artifact


class TestWeb3Provider:

    def test_web3_provider_with_web3_arg(self, default_web3, arbitrary_address):
        instance = BaseContract(artifact_name='ARBITER', web3=default_web3)
        assert instance.provider is not None
        assert default_web3.isConnected() is True

        with pytest.raises(AssertionError):
            assert instance.provider is None
            assert default_web3.isConnected() is False

    def test_web3_provider_with_provider_arg(self):
        w3 = Web3.HTTPProvider('http://127.0.0.1:8545')
        instance = BaseContract(artifact_name='ARBITER', network_provider=w3)
        assert instance.provider is not None
        assert w3.isConnected() is True

        with pytest.raises(AssertionError):
            assert instance.provider is None
            assert w3.isConnected() is False

    def test_web3_provider_with_no_args(self):
        instance = BaseContract(artifact_name='ARBITER', network_id=42)
        assert instance.provider is not None

        with pytest.raises(AssertionError):
            assert instance.provider is None


class TestNetworkId:

    def test_network_id_with_default(self, default_web3):
        instance = BaseContract(artifact_name='ARBITER')
        assert type(instance.network_id) == int
        assert instance.network_id == 1

    @pytest.mark.parametrize('net_id', [42, 31337])
    def test_network_id(self, default_web3, arbitrary_address, net_id):
        instance = BaseContract(artifact_name='ARBITER', web3=default_web3, network_id=net_id,
                                address=arbitrary_address)
        assert type(instance.network_id) == int
        assert instance.network_id == net_id


class TestAddress:

    def test_address(self, default_web3, arbitrary_address):
        instance = BaseContract(artifact_name='ARBITER', web3=default_web3, network_provider=default_web3,
                                address=arbitrary_address)
        assert type(instance.address) == str
        assert instance.address == arbitrary_address

        with pytest.raises(AssertionError):
            assert type(instance.address) != str
            assert instance.address != arbitrary_address

    @pytest.mark.parametrize('input_artifact, expected_address', [
        ('ARBITER', '0x131e22ae3e90f0eeb1fb739eaa62ea0290c3fbe1'),
        ('BONDAGE', '0x188f79b0a8edc10ad53285c47c3feaa0d2716e83'),
        ('DISPATCH', '0xac0f9620c5940085eb5f3a07210d890aa4ceee11'),
        ('REGISTRY', '0xc7ab7ffc4fc2f3c75ffb621f574d4b9c861330f0'),
        ('CurrentCost', '0xde775430f4e9f0df7887d6c7c3ce63b257300fca'),
        ('ZAP_TOKEN', '0x6781a0f84c7e9e846dcb84a9a5bd49333067b104'),
        ('ZAPCOORDINATOR', '0xb007eca49763f31edff95623ed6c23c8c1924a16'),
        ('TOKENDOTFACTORY', '0x2416002d127175bc2d627faefdaa4186c7c49833')
    ])
    def test_address_without_address_arg(self, default_web3, input_artifact, expected_address):
        instance = BaseContract(artifact_name=input_artifact)
        assert instance.address is not None
        assert type(instance.address) == str
        assert instance.address == expected_address

        with pytest.raises(AssertionError):
            assert instance.address is None
            assert type(instance.address) != str
            assert instance.address != expected_address


class TestMethods:

    def test_get_contract_instance(self, mocker):
        instance = BaseContract(artifact_name='ARBITER')
        mocker.patch('base_contract.BaseContract.get_contract', return_value=object)
        assert instance.get_contract() is not None



    @pytest.fixture()
    def mock_get_contract_owner(self, mocker):
        async_mock = AsyncMock()
        mocker.patch('base_contract.get_contract_owner', side_effect=async_mock)
        return async_mock