import configparser
import hashlib

config_file = r'Z:\college\final_capstone\config.ini'

def register(username, password):
    config = configparser.ConfigParser()
    config['Authentication'] = {'Username': username, 'Password': hashlib.sha256(password.encode()).hexdigest()}
    with open(config_file, 'w') as configfile:
        config.write(configfile)
    print("Registration successful.")


# Enter accounts that program will accept
register('username', 'test')
