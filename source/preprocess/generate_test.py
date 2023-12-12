import json
import os
import random

API_PATH = "./dist/json/cloudforet/api"

def list_directories(dir_path) -> list:
    """ List directories
    """
    directories = []
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        directories = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
    return directories

def list_json_file(dir_path) -> list:
    """ List json files
    """
    json_files = []
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        json_files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and f.endswith(".json")]
    return json_files

def parse_json_file(json_file):
    f = open(json_file, 'r')
    data = json.load(f)
    messages = data['files'][0]['messages']
    message_dict = {"Empty": ["True"], "Struct": ["Struct"], "AuthenticationRequest": ["AuthenticationResponse"]}
    for message in messages:
        name = message['name']
        fields = message['fields']
        field_list = []
        for field in fields:
            field_name = field['name']
            field_type = field['type']
            field_list.append(f"{field_name}({field_type})")
        message_dict[name] = field_list 
    
    services = data['files'][0]['services']
    result = {}
    for service in services:
        resource = service['name']
        methods = service['methods']
        verb_list = []
        for method in methods:
            verb  = method['name']
            request = method['requestType']
            response = method['responseType']
            msg_request = message_dict[request] if request in message_dict else []
            msg_response = message_dict[response] if response in message_dict else []

            verb_list.append((verb, msg_request, msg_response))
        result[resource] = verb_list
    return result

def read_micro_service(service_name, version="v1"):
    """ Read micro service
    """
    proto_path = os.path.join(API_PATH, service_name, version)
    json_files = list_json_file(proto_path)
    json_result = []
    for f in json_files:
        r = parse_json_file(os.path.join(API_PATH, service_name, version, f))
        for k, v in r.items():
            for verb in v:
                c = f"spacectl exec {verb[0]} {service_name}.{k}"
                r = {
                    'command' : c,
                    'service': service_name, 
                    'resource': k, 
                    'verb': verb[0], 
                    'request': ",".join(verb[1]), 
                    'response': ",".join(verb[2])}
                json_result.append(r)
    return json_result

def main(result_file="cloudforet_api_train_v2.json", test_file="cloudforet_api_test_v2.json", random_seed=10):
    directories = list_directories(API_PATH)
    json_result = []
    for directory in directories:
        json_result.extend(read_micro_service(directory))
    with open(result_file, "w") as f:
        json.dump(json_result, f, indent=4)
    selected_items = []
    for i in json_result:
        selected_item = random.choice(json_result) if random.random() < 0.1 else None
        if selected_item:
            selected_items.append(selected_item)

    with open(test_file, "w") as f:
        json.dump(selected_items, f, indent=4)
if __name__ == "__main__":
    main()

#with open('User.json') as f:
#    data = json.load(f)
#
#services = data['files'][0]['services']
#methods = services[0]['methods']
#
#for method in methods:
#    print(method['name'])
#
