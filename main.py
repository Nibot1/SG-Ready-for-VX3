import sys
import configparser
import logging
import json
from PyViCare.PyViCare import PyViCare

config = configparser.ConfigParser()
config.read('config.ini')

client_id = config.get('vicare', 'client_id')
email = config.get('vicare', 'email')
password = config.get('vicare', 'password')

vicare = PyViCare()
vicare.initWithCredentials(email, password, client_id, "token.save")
for x in vicare.devices:
  print(x.getModel())
  if(x.getModel() == "E3_HEMS"):
    device = x
    print("Device Model: " + device.getModel())
    print("Status: " + ("Online" if device.isOnline() else "Offline"))
    t = device.asAutoDetectDevice()
    data = {"transfer_power_exchange": t.getTransferPowerExchange}
    print(json.dumps(data))


