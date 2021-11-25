import os
from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

@app.route('/')
def index():
   return 'Server is running...'

if __name__ == '__main__':
   app.run(port=os.getenv('PORT'))
