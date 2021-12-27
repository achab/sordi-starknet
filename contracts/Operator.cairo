%lang starknet
%builtins pedersen range_check

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.hash import hash2
from starkware.starknet.common.syscalls import get_contract_address

# Interfaces

@contract_interface
namespace IWalletContract:
    func set_operator_address(address : felt):
    end

    func transfer_to_phonenumber(phonenumber : felt):
    end
end

@contract_interface
namespace ICurrencyContract:
    func check_wallet(user : felt) -> (balance : felt):
    end
end

# Storage variables

@storage_var
func _phone_to_address(phonenumber : felt) -> (res : felt):
end

@storage_var
func _address_to_phone(address : felt) -> (res : felt):
end

@storage_var
func _passwords(phonenumber : felt) -> (res : felt):
end

# Functions

@external
func add_wallet{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
        contract_address : felt, phonenumber : felt, password : felt):
    alloc_locals
    let (address) = get_contract_address()
    IWalletContract.set_operator_address(contract_address=contract_address, address=address)
    _phone_to_address.write(phonenumber, address)
    _address_to_phone.write(address, phonenumber)
    let (local hashed) = hash2{hash_ptr=pedersen_ptr}(password, 0)
    _passwords.write(phonenumber, hashed)
    return ()
end

@view
func get_wallet_phonenumber{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
        address : felt) -> (phonenumber : felt):
    let (phonenumber) = _address_to_phone.read(address)
    return (phonenumber)
end

@view
func get_wallet_address{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
        phonenumber : felt) -> (address : felt):
    let (address) = _phone_to_address.read(phonenumber)
    return (address)
end

@view
func check_wallet_password{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
        phonenumber : felt, password : felt):
    alloc_locals
    let (local hashed) = hash2{hash_ptr=pedersen_ptr}(password, 0)
    let (local hash_from_mapping) = _passwords.read(phonenumber)
    assert hashed = hash_from_mapping
    return ()
end

@view
func get_wallet_balance{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
        contract_address : felt, phonenumber : felt) -> (balance : felt):
    alloc_locals
    let (local address) = get_wallet_address(phonenumber)
    let (balance) = ICurrencyContract.check_wallet(contract_address=contract_address, user=address)
    return (balance)
end
