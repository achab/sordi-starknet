"""Operator.cairo test file."""
import os

import pytest
from starkware.starknet.testing.starknet import Starknet

CURRENCY_CONTRACT_FILE = os.path.join("contracts", "Currency.cairo")
OPERATOR_CONTRACT_FILE = os.path.join("contracts", "Operator.cairo")
WALLET_CONTRACT_FILE = os.path.join("contracts", "Wallet.cairo")


@pytest.mark.asyncio
async def test_add_wallet():
    """Test add_wallet method."""
    # Create a new Starknet class that simulates the StarkNet
    # system.
    starknet = await Starknet.empty()

    # Deploy contracts.
    operator = await starknet.deploy(
        source=OPERATOR_CONTRACT_FILE,
    )
    wallet = await starknet.deploy(
        source=WALLET_CONTRACT_FILE,
    )

    # Define constants.
    phonenumber = 1234
    password = 5678

    # Add a wallet to the operator.
    await operator.add_wallet(contract_address=wallet.contract_address, phonenumber=phonenumber, password=password).invoke()

    # Check that the phone numbers match.
    execution_info = await operator.get_wallet_phonenumber(address=wallet.contract_address).call()
    assert execution_info.result.phonenumber == phonenumber


@pytest.mark.asyncio
async def test_get_wallet_phonenumber():
    """Test get_wallet_phonenumber method."""
    # Create a new Starknet class that simulates the StarkNet
    # system.
    starknet = await Starknet.empty()

    # Deploy contracts.
    operator = await starknet.deploy(
        source=OPERATOR_CONTRACT_FILE,
    )
    wallet = await starknet.deploy(
        source=WALLET_CONTRACT_FILE,
    )

    # Define constants.
    phonenumber = 1234
    password = 5678

    # Add a wallet to the operator.
    await operator.add_wallet(contract_address=wallet.contract_address, phonenumber=phonenumber, password=password).invoke()

    # Check that the phone numbers match.
    execution_info = await operator.get_wallet_phonenumber(address=wallet.contract_address).call()
    assert execution_info.result.phonenumber == phonenumber


@pytest.mark.asyncio
async def test_get_wallet_address():
    """Test get_wallet_address method."""
    # Create a new Starknet class that simulates the StarkNet
    # system.
    starknet = await Starknet.empty()

    # Deploy contracts.
    operator = await starknet.deploy(
        source=OPERATOR_CONTRACT_FILE,
    )
    wallet = await starknet.deploy(
        source=WALLET_CONTRACT_FILE,
    )

    # Define constants.
    phonenumber = 1234
    password = 5678

    # Add a wallet to the operator.
    await operator.add_wallet(contract_address=wallet.contract_address, phonenumber=phonenumber, password=password).invoke()

    # Check that the addresses match.
    execution_info = await operator.get_wallet_address(phonenumber=phonenumber).call()
    assert execution_info.result.address == wallet.contract_address


@pytest.mark.asyncio
async def test_get_wallet_balance():
    """Test get_wallet_balance method."""
    # Create a new Starknet class that simulates the StarkNet
    # system.
    starknet = await Starknet.empty()

    # Deploy contracts.
    operator = await starknet.deploy(
        source=OPERATOR_CONTRACT_FILE,
    )
    wallet = await starknet.deploy(
        source=WALLET_CONTRACT_FILE,
    )
    currency = await starknet.deploy(
        source=CURRENCY_CONTRACT_FILE,
    )

    # Define constants.
    phonenumber = 1234
    password = 5678

    # Add a wallet to the operator.
    await operator.add_wallet(contract_address=wallet.contract_address, phonenumber=phonenumber, password=password).invoke()

    # Add funds to the wallet
    await currency.register_currency(user=wallet.contract_address, register_amount=30).invoke()

    # Check balances.
    currency_info = await currency.check_wallet(user=wallet.contract_address).call()
    operator_info = await operator.get_wallet_balance(contract_address=currency.contract_address, phonenumber=phonenumber, password=password).call()
    assert currency_info.result.balance == operator_info.result.balance


@pytest.mark.asyncio
async def test_check_wallet_password():
    """Test check_wallet_password method."""
    # Create a new Starknet class that simulates the StarkNet
    # system.
    starknet = await Starknet.empty()

    # Deploy contracts.
    operator = await starknet.deploy(
        source=OPERATOR_CONTRACT_FILE,
    )
    wallet = await starknet.deploy(
        source=WALLET_CONTRACT_FILE,
    )

    # Define constants.
    phonenumber = 1234
    password = 5678
    fake_password = 1111

    # Add a wallet to the operator.
    await operator.add_wallet(contract_address=wallet.contract_address, phonenumber=phonenumber, password=password).invoke()

    # Check that no exception is thrown when password is valid.
    await operator.check_wallet_password(phonenumber=phonenumber, password=password).call()

    # Check that an exception is thrown when password is not valid.
    with pytest.raises(Exception) as e_info:
        await operator.check_wallet_password(phonenumber=phonenumber, password=fake_password).call()
        print(e_info)
