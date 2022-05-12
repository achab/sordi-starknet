from flask import Flask, request, make_response

from menu import Menu
from utils import is_phonenumber_registered


app = Flask(__name__)
port = 5000


@app.route("/", methods=["POST"])
async def ussd_callback():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phonenumber = request.values.get("phoneNumber", None)
    text = request.values.get("text", None)
    network_code = request.values.get("networkCode", None)

    is_registered = await is_phonenumber_registered(phone_number)