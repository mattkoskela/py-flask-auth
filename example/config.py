import os
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("/home/giant/.my.cnf")
db_username = config.get("client", "user")
db_password = config.get("client", "password")
db_hostname = config.get("client", "host")
db_name = "example"
db_uri = "mysql+pymysql://{0}:{1}@{2}/{3}".format(db_username, db_password, db_hostname, db_name)

SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_ECHO = False
SECRET_KEY = "secret_key"
DEBUG = True
BCRYPT_ITERATIONS = 10
