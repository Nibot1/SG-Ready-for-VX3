import sys
import configparser
import logging
import json
from PyViCare.PyViCare import PyViCare

config = configparser.ConfigParser()
config.read("config.ini")

client_id = config.get("vicare", "client_id")
email = config.get("vicare", "email")
password = config.get("vicare", "password")

vicare = PyViCare()
vicare.initWithCredentials(email, password, client_id, "token.save")
for x in vicare.devices:
    if x.getModel() == "E3_HEMS":
        device = x
        t = device.asAutoDetectDevice()
        current_production = t.getPhotovoltaicProductionCurrent()
        if(t.getPhotovoltaicProductionCurrentUnit() == "kilowatt"):
            current_production = int(current_production*1000) #convert kW to W
        
        data = {
            "transfer_power_exchange": t.getPointOfCommonCouplingTransferPowerExchange(),
            "pv-status": t.getPhotovoltaicStatus(),
            "pv-production": current_production,
        }
        print(json.dumps(data))
