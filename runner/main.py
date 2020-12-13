from flask import Flask, jsonify, request
import subprocess
import time
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app)
last_process=None
last_gzserver=None
last_gzweb=None

@app.route("/run_simulation")
def run_sim():
    run_simulation()
    return {
        "res":"ok"
    }
@app.route("/run_code")
def hello():
    all_args = list(request.args.lists())
    args = jsonify(all_args)
    for arg in all_args:
        if arg[0]=="code":
            run_code(arg[1][0])
    print(all_args)
    return(args)

def run_simulation():
    global last_gzserver, last_gzweb
    bashCommand = "roslaunch pr2_gazebo pr2_empty_world.launch"
    if last_gzserver:
        last_gzserver.kill()
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    last_gzserver = process
    time.sleep(2)
    
    bashCommand = "npm start --prefix /root/gzweb"
    if last_gzweb:
        last_gzweb.kill()
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)

    last_gzweb = process
    output, error = process.communicate()

def run_code(code):
    global last_process
    print('CODE', code)
    with open("code.py", "w") as file:
        file.write(code)
    bashCommand = "python3 code.py"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    if last_process:
        last_process.kill()
    last_process = process
    output, error = process.communicate()





if __name__=="__main__":
    app.run(host="0.0.0.0", port=80)
