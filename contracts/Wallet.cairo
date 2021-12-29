%lang starknet
%builtins pedersen range_check

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.starknet.common.syscalls import get_contract_address

# Interfaces

@contract_interface
namespace IOperatorContract:
    func add_wallet(phonenumber : felt, password : felt):
    end

    func get_wallet_phonenumber(address : felt) -> (phonenumber : felt):
    end

    func get_wallet_address(phonenumber : felt) -> (address : felt):
    end
end

@contract_interface
namespace ICurrencyContract:
    func move_currency(from_user : felt, to_user : felt, move_amount : felt):
    end
end

# Storage variables

@storage_var
func _operator_address() -> (res : felt):
end

# Functions

@external
func set_operator_address{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
        address : felt):
    _operator_address.write(address)
    return ()
end

@view
func get_operator_address{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}() -> (
        address : felt):
    let (address) = _operator_address.read()
    return (address)
end

@external
func transfer_to_phonenumber{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
        operator_contract_address : felt, currency_contract_address : felt, phonenumber : felt,
        amount : felt):
    alloc_locals
    let (local to_user) = IOperatorContract.get_wallet_address(
        contract_address=operator_contract_address, phonenumber=phonenumber)
    let (local from_user) = get_contract_address()
    ICurrencyContract.move_currency(
        contract_address=currency_contract_address,
        from_user=from_user,
        to_user=to_user,
        move_amount=amount)
    return ()
end
