import sys
import ConfigParser
import logging
from PyViCare.PyViCare import PyViCare

config = ConfigParser.ConfigParser()
config.readfp(open(r'config.ini'))

client_id = config.get('vicare', 'client_id')
email = config.get('vicare', 'email')
password = config.get('vicare', 'password')

vicare = PyViCare()
vicare.initWithCredentials(email, password, client_id, "token.save")
print(vicare.devices)
device = vicare.devices[0]
print(device.getModel())
print("Online" if device.isOnline() else "Offline")

t = device.asAutoDetectDevice()

