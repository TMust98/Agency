from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
import psycopg2


app = Flask(__name__)
app.config.from_object(Config)
# conn = psycopg2.connect(dbname='agency', user='postgres', password='12345', host='localhost')
conn = psycopg2.connect(dbname='dftss039lkt4oh', user='fyuputsklargyf', password='bfca2a7605ea8f0795a2ada68a0889101e0fdaf23dbea5e987a5a9e52ebeb647', host='ec2-46-137-173-221.eu-west-1.compute.amazonaws.com')
bootstrap = Bootstrap(app)


from app import routes
