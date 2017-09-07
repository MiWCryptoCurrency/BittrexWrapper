from flask import Flask
from flask_cors import CORS
import hmac
import requests
import os
import hashlib
import binascii

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}}) #YOLO CORS -- HARDEN THIS WITH REAL DOMAINS
bittrex_api = "https://bittrex.com/api/v1.1/"
bittrex_api_key = os.environ.get("BITTREX_API")
bittrex_api_secret = os.environ.get("BITTREX_SECRET")

@app.route("/")
def index():
    return "Bittrex API Wrapper for Pinkcoin"

@app.route("/getbalances")
def getbalances():
    result = do_api("account/getbalances")
    return result

@app.route("/getmarketsummaries")
def getmarketsummaries():
    return do_api("/public/getmarketsummaries")

@app.route("/getdeposithistory")
def getdeposithistory():
    return do_api("/account/getdeposithistory")

def do_api(method):
    nonce = binascii.hexlify(os.urandom(16))
    uri = bittrex_api + "%s?apikey=%s&nonce=%s" % (method, bittrex_api_key, nonce)
    h = hmac.new(bittrex_api_secret.encode(), msg=uri.encode(), digestmod=hashlib.sha512)
    sig = h.hexdigest()
    headers = {'apisign': sig}
    print(uri)
    result = requests.get(uri, headers=headers)
    print(result)
    if result.status_code == 200:
    	return result.text
    return "%s" % result.status_code
