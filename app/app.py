from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Jenkins Pipeline is fully functional!, test for pipeline automation.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)