import os
import json
from flask import Flask, jsonify, request, send_from_directory, render_template,redirect,url_for
from flask_cors import CORS
import socket
import json
import struct
import threading
import queue




app = Flask(__name__)
CORS(app)



# Atlas working directory
ATLAS_DIR = 'atlas_apps'
if not os.path.exists(ATLAS_DIR):
    os.makedirs(ATLAS_DIR)

iot_things = {}
iot_things_queue = queue.Queue()
services =[]
services_queue = queue.Queue()
services_ip = {}
service_ip_queue = queue.Queue()




def listen_for_iot_things(iot_things, services):
    # Create a socket object
    # global iot_things
    # global services
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   
    
    # Define the multicast group and port
    multicast_group = '232.1.1.1'
    server_address = ('', 1235)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(server_address)

    # Bind to the server address
    # s.bind(server_address)

    # Tell the operating system to add the socket to the multicast group
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        data, address = s.recvfrom(1024)
        json_data = json.loads(data.decode())
        # print(address[0])

        tweet_type = json_data["Tweet Type"]

       
        if(tweet_type=="Identity_Thing"):
          if(json_data['Thing ID']) not in iot_things:
            iot_things[json_data['Thing ID']]={"Thing ID":json_data['Thing ID'],"Description":json_data['Description'],"Service":[], "IP" : address[0]}
            


        elif (tweet_type=="Service"):
            # print(json_data)
            if json_data['Name'] not in services:
                if json_data["Thing ID"] in iot_things:
                  services.append(json_data['Name'])
                  iot_things[json_data['Thing ID']]['Service'].append(json_data['Name'])
                  iot_things[json_data['Thing ID']]['Service'].sort()
                  services_ip[json_data['Name']] = json_data["Thing ID"]
        iot_things_queue.put(iot_things)
        services_queue.put(services)
        service_ip_queue.put(services_ip)
# Start listening for IoT things in a separate thread
thread = threading.Thread(target=listen_for_iot_things,args=(iot_things,services))
thread.start()



@app.route('/get/things', methods=['GET'])
def get_iot_things():
    iot_things = iot_things_queue.get()
    things_list = list(iot_things.keys())

    things_list.sort()
    ret_dict = {}
    for thing in things_list:
        ret_dict[thing] = iot_things[thing]['Description']
    # print(iot_things,"   ######## ",services)
    return render_template('things.html', things=ret_dict)

@app.route('/get/services', methods=['GET'])
def get_services():
    iot_things = iot_things_queue.get()

    things_list = list(iot_things.keys())

    things_list.sort()
    ret_dict = {}
    for thing in things_list:
        ret_dict[thing] = iot_things[thing]['Service']

    return render_template('services.html', things=ret_dict)


@app.route('/save/app', methods=['POST'])
def save_app():
    data = request.json

    app_name_with_extension = data.get('fileName')
    app_name, _ = os.path.splitext(app_name_with_extension)
    app_data = data.get('appData')
    
    file_path = os.path.join(ATLAS_DIR, f"{app_name}.iot")
    
    with open(file_path, 'w') as file:
        json.dump(app_data, file)
    
    return redirect(url_for('list_apps'))

# 
@app.route('/upload_existing_app', methods=['POST'])
def upload_existing_app():
    file = request.files['appFile']
    content = file.read().decode('utf-8')
    return content


@app.route('/delete/app', methods=['POST'])
def delete_app():
    app_name = request.json.get('filePath')
    print(app_name)
    file_path = os.path.join(ATLAS_DIR, f"{app_name}.iot")
    
    if os.path.exists(file_path):
        os.remove(file_path)
        return redirect(url_for('list_apps'))
    else:
        return jsonify({"status": "error", "message": "App not found"}), 404

@app.route('/list/app', methods=['GET'])
def list_apps():
    apps = []
    
    for filename in os.listdir(ATLAS_DIR):
        if filename.endswith('.iot'):
            apps.append(filename[:-4])
    
    return render_template('apps.html', apps=apps)



@app.route('/activate/app', methods=['POST'])
def activate_app():
    data = request.json
    app_name = data.get('name')
    
    file_path = os.path.join(ATLAS_DIR, f"{app_name}.iot")
    
    if not os.path.exists(file_path):
        return jsonify({"status": "error", "message": "App not found"}), 404
    
    with open(file_path, 'r') as file:
        app_data = json.load(file)
        
    app_type = app_data.get('type')

    if app_type == 'sequential':
        services = app_data.get('services')
        for service in services:
            # Execute each service sequentially
            execute_service(service)
    elif app_type == 'conditional':
        service1 = app_data.get('service1')
        condition = app_data.get('condition')
        service2 = app_data.get('service2')
        conditional_constant = app_data.get('conditional_constant')
        # Execute service1
        output = execute_service(service1)
        
        # Check condition and execute service2 if condition is satisfied
        if check_condition(output, condition, conditional_constant):
            print("Execution Status:",execute_service(service2))
    elif app_type == 'order':
        service1 = app_data.get('service1')
        service2 = app_data.get('service2')
        
        # Execute service1
        execute_service(service1)
        
        # Execute service2
        execute_service(service2)

    return jsonify({"status": "success", "message": "App activated and executed successfully"}), 200

def send_api_call(ip_address, service_name, thing_id):
    port = 6668
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the specified IP address and port
    server_address = (ip_address, port)
    sock.connect(server_address)

    # Construct the API call message
    api_call = {
        "Tweet Type": "Service call",
        "Thing ID": thing_id,#"MySmartThing01",
        "Space ID": "MySmartSpace",
        "Service Name": service_name,
        "Service Inputs": "()"
    }

    # Convert the dictionary to a JSON string
    api_call_json = json.dumps(api_call)

    # Send the API call message
    sock.sendall(api_call_json.encode())

    # Receive the response
    response = sock.recv(1024)
    response_json = json.loads(response.decode())

    # Close the socket
    sock.close()
    
    return response_json['Service Result']

def execute_service(service):
    # Placeholder for executing a service
    print(f"Executing service: {service}")
    services_ip = service_ip_queue.get()
    ip = iot_things_queue.get()[services_ip[service]]['IP']
    service_name = service
    thing_id = services_ip[service]
    # Add your logic to execute the service here
    return send_api_call(ip,service_name, thing_id)

def check_condition(output, condition, conditional_constant):
    # Placeholder for checking condition
    operator_mapping = {
    "==": lambda x, y: x == y,
    ">": lambda x, y: x > y,
    "<": lambda x, y: x < y,
    ">=": lambda x, y: x >= y,
    "<=": lambda x, y: x <= y,
    "!=": lambda x, y: x != y,
    }
    python_condition = operator_mapping.get(condition)
    

    print(f"Checking condition: {condition} with output: {output}")
    # Add your logic to check the condition here
    return python_condition(str(output), str(conditional_constant))  # Placeholder, replace with actual condition check result




@app.route('/stop/app', methods=['POST'])
def stop_app():
    app_name = request.json.get('name')
    
    # Simulate stopping (replace with actual stopping logic)
    # Update a status panel with app status
    return jsonify({"status": "success", "message": f"App '{app_name}' stopped", "app_status": "inactive"}), 200

relationships = {"R1": {"readAmbience": {'1': 'turnLedOn'}}, "R2": {"readAmbience": {'0': 'turnLedOff'}}}
relation_json = [{"relation name": 'R1', "service1": "readAmbience", "service2": "openBlinds", "condition_type": "Conditional", "relationship": "1"},
                  {"relation name": 'R2',"service1": "openBlinds", "service2": "readAmbience", "condition_type": "Order Based", "relationship": ""},
                  {"relation name": 'R3',"service1": "readAmbience", "service2": "turnLightOn", "condition_type": "Conditional", "relationship": "1"},
                  {"relation name": 'R4',"service1": "turnLightOn", "service2": "closeBlinds", "condition_type": "Order", "relationship": ""},
                  {"relation name": 'R5',"service1": "readAmbience", "service2": "turnLedOff", "condition_type": "Conditional", "relationship": "0"},
                  {"relation name": 'R6',"service1": "readAmbience", "service2": "closeBlinds", "condition_type": "Conditional", "relationship": "0"}]
@app.route('/relations')
def relations():
    services = services_queue.get()
    return render_template('relations.html', services=services, relationships=relation_json)



if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port=5000)