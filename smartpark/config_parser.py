"""A class or function to parse the config file and return the values as a dictionary.

The config file itself can be any of the following formats (recommend one of pandas, json, or ryo):

- You can use pandas to read a data file if you like. Something simple like a CSV would be best.

- ryo: means 'roll your own' and is a simple text file with key-value pairs separated by an equals sign. For example:
```
location = "Moondalup City Square Parking"
number_of_spaces = 192
```
**you** read the file and parse it into a dictionary.
- json: a json file with key-value pairs. For example:
```json
{location: "Moondalup City Square Parking", number_of_spaces: 192}
```
json is built in to python, so you can use the json module to parse it into a dictionary.
- toml: a toml file with key-value pairs. For example:
```toml
[location]
name = "Moondalup City Square Parking"
spaces = 192
```
toml is part of the standard library in python 3.11, otherwise you need to install tomli to parse it into a dictionary.
```bash
python -m pip install tomli
```
see [realpython.com](https://realpython.com/python-toml/) for more info.

Finally, you can use `yaml` if you prefer.



"""
import os


def parse_config(config_file: str) -> dict:
    """Parse the config file and return the values as a dictionary"""
    # receiving carpark_config.txt

    script_dir = os.path.dirname(os.path.abspath(__file__))  # folder of this script
    config_path = os.path.join(script_dir, config_file)

    with open(config_path,"r") as file:
        lines = file.readlines()

    # read the data into a list
    config = {}

    for line in lines:
        line = line.strip()
        if "=" in line:
            key,value = line.split("=",1)  # splits each line into key and value only once (in case the value contains =).
            config[key.strip()] = value.strip()

    location = config.get("location")
    total_spaces = int(config.get("total_spaces",0))
    log_file = config.get("log_file")
    return {'location': location, 'total_spaces': total_spaces, 'log_file':log_file }