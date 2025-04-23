from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO
import json
from markupsafe import escape
# from gpiozero import LED

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
plansFile="plans/plans.json"
outputsFile="outputs.json"

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

@app.route("/plans")
def plans():
    f=open(plansFile)
    plans=json.load(f)

    return render_template('plans.html', plans=plans['plans'])

@app.route("/plans/edit/<plan>", methods=['GET', 'POST'])
def editPlan(plan):
    toEdit = escape(plan)
    if request.method == 'GET':
        f=open(plansFile)
        plans=json.load(f)['plans']
        f.close()

        f=open(outputsFile)
        outputs=json.load(f)["outputs"]
        valves=[]
        for output in outputs:
            if output["inUse"]:
                valves.append(output)
        f.close()

        for plan in plans:
            if plan["planName"]==toEdit:
                return render_template('editPlan.html', plan=plan, valves=valves)
            
        return f"There is no plan {toEdit} :(("
    elif request.method == 'POST':
        isActive = request.form.get('isActive')
        if not isActive:
            isActive=False
        else:
            isActive=True

        planName = request.form.get('planName')
        weekDays = request.form.getlist('weekDays')
        startTime = request.form.get('startTime')

        sections = []
        i=0
        while True:
            name = request.form.get(f"sections[{i}][name]")
            if not name:
                break
            valves = list(map(int,request.form.getlist(f"sections[{i}][valves][]")))
            duration = int(request.form.get(f"sections[{i}][duration]"))
            
            sections.append({
                'name': name,
                'valves': valves,
                'duration': duration
            })

            i+=1

        planToSave={
            'planName': planName,
            'startTime': startTime,
            'weekDays': weekDays,
            'isActive': isActive,
            'sections':sections
        }

        saveEditedPlan(planToSave, plansFile, toEdit)
        return redirect(f"/plans/edit/{planName}")



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

def saveEditedPlan(planToSave, plansFile, toEdit):
    f=open(plansFile)
    plans=json.load(f)['plans']
    f.close()

    i=0
    for plan in plans:
        if plan["planName"]==toEdit:
            break
        i+=1
    plans.pop(i)
    plans.append(planToSave)

    toSave={
        "plans":plans
    }

    f=open(plansFile,'w')
    f.write(json.dumps(toSave))
    f.close()


if __name__ == '__main__':
    socketio.run(app)