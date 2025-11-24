from interfaces import CarparkSensorListener
from interfaces import CarparkDataProvider
from config_parser import parse_config
import time
import json
import os

class CarparkManager(CarparkSensorListener,CarparkDataProvider):
    CONFIG_FILE = "carpark_config.txt"

    def __init__(self):
        configuration = parse_config(CarparkManager.CONFIG_FILE)
        print("config_file.txt is read")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.location = configuration.get("location")
        self.total_spaces = configuration.get("total_spaces")
        self.log_file = os.path.join(script_dir, configuration.get("log_file"))
        self._temperature_value = 0.0  # store temperature value here rather than in the log
        self.active_cars = {}  # key = license plate, value = Car instance, manage car in the carpark
        self._display = None

        # insert initial data to log file so the available spaces can access it to calculate
        initial_log_data = {
            "available_spaces": self.total_spaces,
            "license_plate": None,
            "enter_time": None,
            "exit_time": None
        }
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as file:
                json.dump([initial_log_data], file, indent=4)
            print(f"Log file created: {self.log_file}")
        else:
            print(f"Log file {self.log_file} already exist!")

    
    @property
    def available_spaces(self):
        """
            Get the latest value of available_spaces (the newest updated value)
            Not saved as a variable, like temperature, to avoid the value restart from total spaces
            in the case of app crash. Reading from the log so the latest value can be received.
            If user wants to restart the count, can just delete/rename the log and start from the new number
        """
        with open(self.log_file, "r") as file:
            data = json.load(file)
        
        for record in data:
            if record.get("available_spaces") is not None:
                if record.get("available_spaces") > 0:
                    return record.get("available_spaces")
                else:
                    return 0
        return None
    
    @property
    def temperature(self):
        return self._temperature_value

    @property
    def current_time(self):
        return time.localtime()

    # register the display instance here so they are hooked
    def register_display(self,display):
        self._display = display    
    
    
    def incoming_car(self,license_plate):
        """
            Check if the car already exist, if yes, then return error
            If not exist, then write to the log and update the available space
            Call the update_display method to update the display
        """
        license_plate = license_plate.strip().upper()  # standardized
        car = self.active_cars.get(license_plate)
        # check if car already exist
        if not car:
            car = Car()
            car.license_plate = license_plate.strip().upper()
            car.entry_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            self.active_cars[car.license_plate] = car
            
            print(f"Car {car.license_plate} entered at {car.entry_time}")

            with open(self.log_file, "r") as file:
                data = json.load(file)
            
            # update available_space and log the incoming car event
            new_entry = {
                "available_spaces": self.available_spaces -1,
                "license_plate": car.license_plate,
                "enter_time": car.entry_time,
                "exit_time": None
            }

            # insert with index 0 so it's at the top of the file
            data.insert(0,new_entry)

            with open(self.log_file, "w") as file:
                json.dump(data, file, indent=4)

            print(car.license_plate, "entered and logged")

        else:
            print(f"Car {license_plate} already in!  ")

        # update the display
        if self._display is not None:
            self._display.update_display()



    def outgoing_car(self,license_plate):
        """
            Check if the car exist, if no, then return error
            If it exists, then write to the log and update the available space
            Call the update_display method to update the display
        """

        license_plate = license_plate.strip().upper()
        car = self.active_cars.get(license_plate)

        # check if car already exist
        if not car:
            print(f"Error: Car {license_plate} not found")
            return
        
        car.exit_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

        print(f"Car {car.license_plate} left at {car.exit_time}")
        
        with open(self.log_file, "r") as file:
            data = json.load(file)
        
        # update available_space and log the outgoing car event
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

        # remove car from active_cars
        del self.active_cars[car.license_plate]

        # update the display
        if self._display is not None:
            self._display.update_display()

    def temperature_reading(self,reading):
        self._temperature_value = float(reading)
        print(f'temperature is updated to {reading}')        

        # return self._temperature_value
    
        if self._display is not None:
            self._display.update_display()

class Car:
    """
        Car, contains: 
        - license plate
        - entry time
        - exit time
    """
    def __init__(self,plate=None):
        self.license_plate = plate
        self.entry_time = None
        self.exit_time = None