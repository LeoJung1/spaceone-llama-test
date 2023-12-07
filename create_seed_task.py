import json
import os
import random
from collections import defaultdict

API_PATH = "./dist/json/cloudforet/api"

def list_directories(dir_path) -> list:
    """ 
    List directories
    """
    directories = []
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        directories = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
    return directories

def list_json_file(dir_path) -> list:
    """ 
    List json files
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
    """ 
    Read micro service and generate resource dictionary
    """
    ms_structure = defaultdict(dict)
    proto_path = os.path.join(API_PATH, service_name, version)
    json_files = list_json_file(proto_path)
    for f in json_files:
        r = parse_json_file(os.path.join(API_PATH, service_name, version, f))
        for k, v in r.items():
            for verb in v:
                ms_structure[f"{service_name}.{k}"][verb[0]] = {"request" : verb[1], "response" : verb[2]}
    return ms_structure
                
def extract_microservice(spaceone_structure):
    """
    Extract the microservices
    """

    return list(spaceone_structure.keys())

def extract_resources(spaceone_structure, microservice : str):
    """
    Extract the Resources
    """

    return list(spaceone_structure[microservice].keys())

def extract_verbs(spaceone_structure, microservice : str, resource : str):
    """
    Extract the possible verbs for the resource
    """

    return list(spaceone_structure[microservice][resource].keys())

def extract_verb_request_response(spaceone_structure, microservice : str, resource : str, verb : str):
    """
    Show the required params for the request and the response using the verbs
    """

    required_param = spaceone_structure[microservice][resource][verb]["request"]
    response_param = spaceone_structure[microservice][resource][verb]["response"] 
    return required_param, response_param

def microservice_instruct():
    instruction_1 = "What microservices exist in the SpaceOne?"
    instruction_2 = "Give me all the microservices in SpaceOne"
    instruction_3 = "What specific microservicse form part of SpaceOne's architecture?"
    return {"inst_1" : instruction_1, "inst_2" : instruction_2, "inst_3" : instruction_3}

def resource_instruct(microservice):
    instruction_1 = f"What resources are in {microservice} microservice?"
    instruction_2 = f"List all the resources that are existing in the inputted microservice"
    instruction_3 = f"In the {microservice} microservice, what resources are there?"
    instruction_4 = f"Name all the resources existing in the {microservice} microservice"
    instruction_5 = f"Show me all the resources that are existing in the following microservice"
    return {"inst_1" : instruction_1, "inst_2" : instruction_2, "inst_3" : instruction_3, "inst_4" : instruction_4, "inst_5" : instruction_5}

def verb_instruct(resource):
    instruction_1 = f"What are the executable verbs existing in the {resource} resource?"
    instruction_2 = f"I want to know the possible executable verbs of the following resource"
    instruction_3 = f"What verbs can I use for the {resource} resource?"
    instruction_4 = f"List all the verbs that I can utilize for the {resource} resource"
    instruction_5 = f"Outline all the verbs that are existent in the following resource"
    return {"inst_1" : instruction_1, "inst_2" : instruction_2, "inst_3" : instruction_3, "inst_4" : instruction_4, "inst_5" : instruction_5}


def parameter_instruct(resource, verb):
    instruction_1 = f"""Show me the parameters required to execute "{verb}" in {resource} resource"""
    instruction_2 = f"""What parameters are needed to execute the following verb in the resource?"""
    instruction_3 = f"""I want to execute "{verb}" in the {resource} resource. What are the required parameters?"""
    instruction_4 = f"""What schemas do I need to execute the "{verb}" verb for the {resource} resource?"""
    instruction_5 = f"""List out the required parameters need for the execution of the following verb in the resource"""

    instruction_6 = f"""Show me the resulting parameters when I execute "{verb}" in the {resource} resource"""
    instruction_7 = f"""What do I get when I execute the following verb in the resource?"""
    instruction_8 = f"""What is the response that I get when I execute "{verb}" in {resource} resource?"""
    instruction_9 = f"""What kind of variables will I get as a response when I use "{verb}" in {resource}? """
    instruction_10 = f"""For executing the following verb in its resource, what is the response that I will get?"""
    return {"inst_1" : instruction_1, "inst_2" : instruction_2, "inst_3" : instruction_3, "inst4" : instruction_4, "inst_5" : instruction_5, 
            "inst_6" : instruction_6, "inst_7": instruction_7, "inst_8" : instruction_8, "inst_9" : instruction_9, "inst_10" : instruction_10}

def main():
    output_file = "seed_task_data.jsonl"
    spaceone_structure = defaultdict(dict)
    directories = list_directories(API_PATH)
    for directory in directories:
        spaceone_structure[directory] = read_micro_service(directory)
    
    seed_count = 0
    result = []
    microservice_instructions = microservice_instruct()
    for instruction in microservice_instructions:
        line = {
            "id" : f"seed_task_{seed_count}",
            "name" : "search_microservice",
            "instruction" : microservice_instructions[instruction],
            "instances" : [{"input" : "", "output" : ", ".join(extract_microservice(spaceone_structure))}]
            }
        result.append(line)
        seed_count += 1
        
    for microservice in spaceone_structure:

        for resource in spaceone_structure[microservice]:
            resource_instruction = resource_instruct(microservice)
            output = ", ".join(extract_resources(spaceone_structure, microservice))
            # Create instruction for resources
            for instruction in resource_instruction:
                if instruction == "inst_2" or instruction == "inst_5":
                    res_instances = [{"input" : microservice, "output": output}]
                else:
                    res_instances = [{"input" : "", "output":output}]
                resource_line = {
                    "id" : f"seed_task_{seed_count}",
                    "name" : f"search_resource",
                    "instruction" : resource_instruction[instruction],
                    "instances" : res_instances
                }
                result.append(resource_line)
                seed_count += 1

            for verb in spaceone_structure[microservice][resource]:
                verb_instruction = verb_instruct(resource)
                parameter_instruction = parameter_instruct(resource, verb)
                verb_output = extract_verbs(spaceone_structure, microservice, resource)
                parameter_request, parameter_response = extract_verb_request_response(spaceone_structure, microservice, resource, verb)
                for instruction in verb_instruction:
                    if instruction == "inst_2" or instruction == "inst_5":
                        v_instances = [{"input" : resource, "output": verb_output}]
                    else:
                        v_instances = [{"input":"", "output": verb_output}]
                    verb_line = {
                        "id" : f"seed_task_{seed_count}",
                        "name" : f"search_verb",
                        "instruction" : verb_instruction[instruction],
                        "instances" : v_instances,
                    }
                    result.append(verb_line)
                    seed_count += 1
                for instruction in parameter_instruction:
                    if instruction == "inst_2" or instruction == "inst_5":
                        par_instances = [{"input" : f"Resource : {resource}, Verb : {verb}", "output": parameter_request}]
                    elif instruction in ["inst_1", "inst_3", "inst_4"]:
                        par_instances = [{"input" : "", "output" : parameter_request}]
                    elif instruction == "inst_6" or instruction == "inst_10":
                        par_instances = [{"input" : f"Resource : {resource}, Verb : {verb}", "output" : parameter_response}]
                    else:
                        par_instances = [{"input" : "", "output": parameter_response}]
                    param_line = {
                        "id" : f"seed_task_{seed_count}",
                        "name" : f"search_parameters",
                        "instruction" : parameter_instruction[instruction],
                        "instances" : par_instances,
                    }
                    result.append(param_line)
                    seed_count += 1
                        
                
    with open(output_file, "w") as f:
        random.shuffle(result)
        json.dump(result, f, indent=4)

    seed_task_test_file = "seed_task_test.jsonl"
    selected_items = []
    for i in result:
        selected_item = random.choice(result) if random.random() < 0.1 else None
        if selected_item:
            selected_items.append(selected_item)

    with open(seed_task_test_file, "w") as f:
        json.dump(selected_items, f, indent=4)
        

if __name__ == "__main__":
    main()
