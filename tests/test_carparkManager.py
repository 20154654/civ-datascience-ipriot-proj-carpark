import os
import json
import sys
import unittest

# this is to make sure 
# the tests treat the smartpark folder as if it were the current directory
CURRENT_DIR = os.path.dirname(__file__)
SMARTPARK_DIR = os.path.join(CURRENT_DIR, "..", "smartpark")
sys.path.insert(0, os.path.abspath(SMARTPARK_DIR))

import smartpark.carparkManager
from smartpark.carparkManager import CarparkManager


class TestCarparkManager(unittest.TestCase):

    def setUp(self):
        """
        start with a clean log file
        pass fake parse_config() to CarparkManager
        """
        # keep the setting for restoring later
        self._original_parse_config = smartpark.carparkManager.parse_config

        def fake_parse_config(_):
            # This is what your config file would normally return
            return {
                "location": "Test carpark",
                "total_spaces": 5,
                "log_file": "test_log.json",
            }

        smartpark.carparkManager.parse_config = fake_parse_config

        # make sure the log file is clean
        self.script_dir = os.path.dirname(os.path.abspath(smartpark.carparkManager.__file__))
        self.log_path = os.path.join(self.script_dir, "test_log.json")
        if os.path.exists(self.log_path):
            os.remove(self.log_path)
                   
        self.manager = CarparkManager()

    def tearDown(self):
        # remove any logfile generated during test, just in case
        smartpark.carparkManager.parse_config = self._original_parse_config
        if os.path.exists(self.log_path):
            os.remove(self.log_path)

    def _read_log(self):
        with open(self.log_path, "r") as file:
            return json.load(file)
    
    def test_initial_available_spaces(self):
        log_data = self._read_log()

        # initial available space should be 5
        self.assertEqual(self.manager.total_spaces, 5)
        self.assertEqual(self.manager.available_spaces, 5)
        self.assertEqual(log_data[0]["available_spaces"], 5)

    def test_incoming_car_reduce_available_spaces(self):
        self.manager.incoming_car("ABC123")
        log_data = self._read_log()

        # available space should be 4
        self.assertEqual(self.manager.available_spaces, 4)
        self.assertEqual(log_data[0]["available_spaces"], 4)
        
        # car license plate should exist in active_cars
        self.assertIn("ABC123", self.manager.active_cars)
        car = self.manager.active_cars["ABC123"]
        self.assertIsNotNone(car.entry_time)


if __name__ == '__main__':
    unittest.main()


        
