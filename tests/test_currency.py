"""Currency.cairo test file."""
import os

import pytest
from starkware.starknet.testing.starknet import Starknet

# The path to the contract source code.
CONTRACT_FILE = os.path.join("contracts", "Currency.cairo")


@pytest.mark.asyncio
async def test_register_currency():
    """Test register_currency method."""
    # Create a new Starknet class that simulates the StarkNet
    # system.
    starknet = await Starknet.empty()

    # Deploy the contract.
    contract = await starknet.deploy(
        source=CONTRACT_FILE,
    )

    # Define a user.
    user = 1234

    # Invoke register_currency().
    await contract.register_currency(user=user, register_amount=10).invoke()

    # Check the result of get_balance().
    execution_info = await contract.check_wallet(user=user).call()
    assert execution_info.result == (10,)


@pytest.mark.asyncio
async def test_move_currency():
    """Test move_currency method."""
    # Create a new Starknet class that simulates the StarkNet
    # system.
    starknet = await Starknet.empty()

    # Deploy the contract.
    contract = await starknet.deploy(
        source=CONTRACT_FILE,
    )

    # Define users.
    from_user = 1234
    to_user = 5678

    # Invoke register_currency().
    await contract.register_currency(user=from_user, register_amount=30).invoke()
    await contract.register_currency(user=to_user, register_amount=10).invoke()

    # Invoke move_currency().
    await contract.move_currency(from_user=from_user, to_user=to_user, move_amount=5).invoke()

    # Check results of get_balance().
    execution_info = await contract.check_wallet(user=from_user).call()
    assert execution_info.result == (25,)
    execution_info = await contract.check_wallet(user=to_user).call()
    assert execution_info.result == (15,)
