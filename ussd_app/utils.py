import os

from dotenv import load_dotenv

from starknet.contract import Contract
from starknet.net.client import Client

load_dotenv()
NETWORK = os.getenv("NETWORK")


def get_deployments_filename():
    if NETWORK == "":
        fname = "localhost.deployments.txt"
    elif NETWORK == "testnet":
        fname = "goerli.deployments.txt"
    elif NETWORK == "mainnet":
        fname = "mainnet.deployments.txt"
    else:
        raise ValueError(f"Network name is not valid. Current value is {NETWORK}.")
    return fname

def format_phonenumber(phonenumber: str):
  return phonenumber.replace("+", "00")

def get_latest_deployment_address(name: str):
    fname = get_deployments_filename()
    lines = open(fname, "r").readlines()
    for line in lines:
        if name in line:
            return line.split(":")[0]
    raise ValueError(f"Contract {name} has not been deployed yet on the network {fname.split('.')[0]}.")