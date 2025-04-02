from flask import Flask, render_template, request
from flask_socketio import SocketIO
import json
# from gpiozero import LED

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

class output:
    def __init__(self, gpio, status):
        self.gpio = gpio
        self.status = status
        #self.out = LED(gpio)
    
    def __str__(self):
        return f"GPIO {self.gpio}, status: {self.status}"

outputs=[]
for i in range(0,28):
    outputs.append(output(i,0))

@app.route("/")
def index():
    f = open("outputs.json")
    outputsJson=json.load(f)

    return render_template('index.html', outputs=outputsJson['outputs'])

@socketio.on('connect')
def handleConnect():
    print("Client connected")
    sessionId = request.sid
    updateStatusesMessage(sessionId)

@socketio.on('change')
def handleValveChange(data):
    gpio = int(data[-2])
    status = int(data[-1])
    outputs[gpio].status=status
    updateStatusesMessage()

def updateStatusesMessage(sessionId=None):
    if sessionId:
        for output in outputs:
            messageData = output.__dict__
            messageData = json.dumps(messageData)
            socketio.emit('initialStatuses', messageData, to=sessionId)
    else:
        for output in outputs:
            messageData = output.__dict__
            messageData = json.dumps(messageData)
            socketio.emit('statusChanged', messageData)

if __name__ == '__main__':
    socketio.run(app)