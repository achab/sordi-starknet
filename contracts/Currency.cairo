%lang starknet
%builtins pedersen range_check

from starkware.cairo.common.cairo_builtins import HashBuiltin

@storage_var
func wallet_balance(user : felt) -> (res : felt):
end

@external
func register_currency{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
        user : felt, register_amount : felt):
    alloc_locals
    let (local balance) = wallet_balance.read(user)
    wallet_balance.write(user, balance + register_amount)
    return ()
end

@external
func move_currency{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
        from_user : felt, to_user : felt, move_amount : felt):
    alloc_locals
    let (local sender_balance) = wallet_balance.read(from_user)
    let (local receiver_balance) = wallet_balance.read(to_user)
    wallet_balance.write(to_user, receiver_balance + move_amount)
    wallet_balance.write(from_user, sender_balance - move_amount)
    return ()
end

@view
func check_wallet{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
        user : felt) -> (balance : felt):
    alloc_locals
    let (local balance) = wallet_balance.read(user)
    return (balance)
end
