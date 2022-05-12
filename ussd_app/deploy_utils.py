import json
import os


def get_abi(contract_name: str):
  filename = os.getcwd() + f"/../artifacts/abis/{contract_name}.json"
  abi = json.load(open(filename))
  return abi

def get_currency_abi():
    return get_abi("Currency")

def get_operator_abi():
    return get_abi("Operator")

def get_wallet_abi():
    return get_abi("Wallet")
