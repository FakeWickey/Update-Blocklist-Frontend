import json
import configparser

with open('credentialdb.json', 'r') as json_file:
    json_data = json.load(json_file)

config = configparser.ConfigParser()
config['DEFAULT'] = json_data

with open('output.ini', 'w') as ini_file:
    config.write(ini_file)
