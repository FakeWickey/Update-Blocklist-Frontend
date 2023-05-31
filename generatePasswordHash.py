import sys, hashlib, configparser, os

if len(sys.argv) < 2:
   print('Usage: python generatePasswordHash.py [password]')
   sys.exit(1)

password = sys.argv[1]

config = configparser.ConfigParser()
config.read('config.ini')

salt = config.get('internal', 'salt')
pepper = config.get('internal', 'pepper')


salted_and_peppered_password = password + salt + pepper

hashed_password = hashlib.sha256(salted_and_peppered_password.encode('utf-8')).hexdigest()
print(f'This is the hashed password: {hashed_password}\nPlace it as the password_hashed value in config.ini')

