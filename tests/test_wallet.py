"""Wallet.cairo test file."""
import os

import pytest
from starkware.starknet.testing.starknet import Starknet

CURRENCY_CONTRACT_FILE = os.path.join("contracts", "Currency.cairo")
OPERATOR_CONTRACT_FILE = os.path.join("contracts", "Operator.cairo")
WALLET_CONTRACT_FILE = os.path.join("contracts", "Wallet.cairo")


@pytest.mark.asyncio
async def test_set_operator_address():
    # Create a new Starknet class that simulates the StarkNet
    # system.
    """Test set_operator_address method."""
    starknet = await Starknet.empty()

    # Deploy contracts.
    operator = await starknet.deploy(
        source=OPERATOR_CONTRACT_FILE,
    )
    wallet = await starknet.deploy(
        source=WALLET_CONTRACT_FILE,
    )

    # Set operator address
    operator_address = operator.contract_address
    await wallet.set_operator_address(address=operator_address).invoke()

    # Check that the phone numbers match.
    execution_info = await wallet.get_operator_address().call()
    assert execution_info.result.address == operator_address


@pytest.mark.asyncio
async def test_transfer_to_phonenumber():
    # Create a new Starknet class that simulates the StarkNet
    # system.
    """Test transfer_to_phonenumber method."""
    starknet = await Starknet.empty()

    # Deploy contracts.
    operator = await starknet.deploy(
        source=OPERATOR_CONTRACT_FILE,
    )
    wallet1 = await starknet.deploy(
        source=WALLET_CONTRACT_FILE,
    )
    wallet2 = await starknet.deploy(
        source=WALLET_CONTRACT_FILE,
    )
    currency = await starknet.deploy(
        source=CURRENCY_CONTRACT_FILE,
    )

    # Define constants.
    phonenumber1 = 1234
    password1 = 5678
    phonenumber2 = 4321
    password2 = 8765

    # Add wallets to the operator.
    await operator.add_wallet(contract_address=wallet1.contract_address, phonenumber=phonenumber1, password=password1).invoke()
    await operator.add_wallet(contract_address=wallet2.contract_address, phonenumber=phonenumber2, password=password2).invoke()

    # Add funds to the wallets
    await currency.register_currency(user=wallet1.contract_address, register_amount=30).invoke()
    await currency.register_currency(user=wallet2.contract_address, register_amount=10).invoke()

    # Transfer funds using phone numbers
    await wallet1.transfer_to_phonenumber(operator_contract_address=operator.contract_address, currency_contract_address=currency.contract_address, phonenumber=phonenumber2, amount=5).invoke()

    # Check balances.
    execution_info = await currency.check_wallet(user=wallet1.contract_address).call()
    assert execution_info.result.balance == 25
    execution_info = await currency.check_wallet(user=wallet2.contract_address).call()
    assert execution_info.result.balance == 15


