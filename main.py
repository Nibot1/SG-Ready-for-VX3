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

try:
    vicare = PyViCare()
    vicare.initWithCredentials(email, password, client_id, "token.save")
    if len(sys.argv) >= 2 and sys.argv[1] == "dhw-temperature":
            device = vicare.devices[0]
            t= device.asAutoDetectDevice()
            data = {
                "result":"ok",
                "dhw_storage_temperature": t.getDomesticHotWaterStorageTemperature()
            }
            print(json.dumps(data))
    else:
        for x in vicare.devices:
            if x.getModel() == "E3_VitoCharge_03":
                device = x
                t = device.asAutoDetectDevice()
                current_production = t.getPhotovoltaicProductionCurrent()
                ees_current_power = t.getElectricalEnergySystemPower()
                if t.getPhotovoltaicProductionCurrentUnit() == "kilowatt":
                    current_production = int(current_production * 1000)  # convert kW to W
                if t.getElectricalEnergySystemPowerUnit() == "kilowatt":
                    ees_current_power = int(ees_current_power * 1000)  # convert kW to W

                data = {
                    "result": "ok",
                    "transfer_power_exchange": t.getPointOfCommonCouplingTransferPowerExchange(),
                    "pv_status": t.getPhotovoltaicStatus(),
                    "pv_production": current_production,
                    "ees_current_discharge": ees_current_power,
                }
                print(json.dumps(data))
except:
    output = { "result": "error" }
    print(json.dumps(output))
