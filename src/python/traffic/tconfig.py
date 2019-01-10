import configparser
import os

keys_config = configparser.ConfigParser()
keys_config.read(os.path.abspath(os.path.join(__file__, '..', '..', '..', '..', '_private', 'keys.config')))

db_config = configparser.ConfigParser()
db_config.read(os.path.abspath(os.path.join(__file__, '..', '..', '..', '..', '_private', 'db.config')))