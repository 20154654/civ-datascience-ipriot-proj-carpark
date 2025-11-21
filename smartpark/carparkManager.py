from interfaces import CarparkSensorListener
from interfaces import CarparkDataProvider
from config_parser import parse_config
import time
import json
import os

class CarparkManager(CarparkSensorListener,CarparkDataProvider):
    #constant, for where to get the configuration data
    CONFIG_FILE = "carpark_config.txt"

    def __init__(self):
        configuration = parse_config(CarparkManager.CONFIG_FILE)
        print("config_file.txt is read")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.location = configuration.get("location")
        self.total_spaces = configuration.get("total_spaces")
        self.log_file = os.path.join(script_dir, configuration.get("log_file"))
        self._temperature_value = 0.0
        self.active_cars = {}  # key = license plate, value = Car instance
        self._display = None


        initial_log_data = {
            "available_spaces": self.total_spaces,
            "license_plate": None,
            "enter_time": None,
            "exit_time": None
        }
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as file:
                json.dump([initial_log_data], file, indent=4)
            print(f"Log file crated: {self.log_file}")
        else:
            print(f"Log file {self.log_file} already exist!")

    
    @property
    def available_spaces(self):
        with open(self.log_file, "r") as file:
            data = json.load(file)

        for record in data:
            if record.get("available_spaces") is not None:
                return record.get("available_spaces")
            
        return None
    
    @property
    def temperature(self):
        return self._temperature_value

    @property
    def current_time(self):
        return time.localtime()


    def register_display(self,display):
        self._display = display    
    
    
    def incoming_car(self,license_plate):
        license_plate = license_plate.strip().upper()
        car = self.active_cars.get(license_plate)
        if not car:
            car = Car()
            car.license_plate = license_plate.strip().upper()
            car.entry_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            self.active_cars[car.license_plate] = car
            
            print(f"Car {car.license_plate} entered at {car.entry_time}")

            with open(self.log_file, "r") as file:
                data = json.load(file)
            
            new_entry = {
                "available_spaces": self.available_spaces -1,
                "license_plate": car.license_plate,
                "enter_time": car.entry_time,
                "exit_time": None
            }

            data.insert(0,new_entry)

            with open(self.log_file, "w") as file:
                json.dump(data, file, indent=4)

            print(car.license_plate, "entered and logged")

        else:
            print(f"Car {license_plate} already in!  ")

        if self._display is not None:
            self._display.update_display()



    def outgoing_car(self,license_plate):
        license_plate = license_plate.strip().upper()
        car = self.active_cars.get(license_plate)

        if not car:
            print(f"Error: Car {license_plate} not found")
            return
        
        car.exit_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

        print(f"Car {car.license_plate} left at {car.exit_time}")
        
        with open(self.log_file, "r") as file:
            data = json.load(file)
        
        new_entry = {
            "available_spaces": self.available_spaces +1,
            "license_plate": car.license_plate,
            "enter_time": None,
            "exit_time": car.exit_time
        }

        data.insert(0,new_entry)

        with open(self.log_file, "w") as file:
            json.dump(data, file, indent=4)

        print(car.license_plate, "removed and logged")

        del self.active_cars[car.license_plate]

        if self._display is not None:
            self._display.update_display()

    def temperature_reading(self,reading):
        self._temperature_value = float(reading)
        print(f'temperature is updated to {reading}')        

        # return self._temperature_value
    
        if self._display is not None:
            self._display.update_display()

class Car:
    def __init__(self,plate=None):
        self.license_plate = plate
        self.entry_time = None
        self.exit_time = None