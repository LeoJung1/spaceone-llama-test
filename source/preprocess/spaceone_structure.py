import os
import json
from collections import defaultdict


class SpaceoneStructure:
    API_PATH = "./api-doc/dist/json/cloudforet/api"

    def __init__(self):
        self.structure = defaultdict(dict)
        self.microservices = self._list_directories(SpaceoneStructure.API_PATH)
        for microservice in self.microservices:
            self.structure[microservice] = self._read_micro_service(microservice)

    def _list_directories(self, dir_path : str) -> list:
        """ 
        List directories
        """
        directories = []
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            directories = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
        return directories

    def _list_json_file(self,dir_path : str) -> list:
        """ 
        List json files
        """
        json_files = []
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            json_files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and f.endswith(".json")]
        return json_files

    def _parse_json_file(self, json_file) -> dict:
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


    def _read_micro_service(self, service_name : str, version="v1") -> dict:
        """ 
        Read micro service and generate resource dictionary
        """
        ms_structure = defaultdict(dict)
        proto_path = os.path.join(SpaceoneStructure.API_PATH, service_name, version)
        json_files = self._list_json_file(proto_path)
        exclude = set(["identity.Authorization.verify", "inventory.Job.get", "identity.Domain.get_public_key", "cost_analysis.DataSource.sync"])
        for f in json_files:
            r = self._parse_json_file(os.path.join(SpaceoneStructure.API_PATH, service_name, version, f))
            for k, v in r.items():
                for verb in v:
                    current = f"{service_name}.{k}.{verb[0]}"
                    if current in exclude:
                        continue
                    ms_structure[f"{service_name}.{k}"][verb[0]] = {"request" : verb[1], "response" : verb[2]}
        return ms_structure
                
    def extract_microservice(self) -> list:
        """
        Extract the microservices in SpaceOne
        """

        return self.microservices 

    def extract_resources(self, microservice : str) -> list:
        """
        Extract the resources in the microservice
        """

        return self.structure[microservice].keys()

    def extract_verbs(self, microservice : str, resource : str) -> list:
        """
        Extract the possible verbs for the resource
        """

        return self.structure[microservice][resource].keys()

    def extract_verb_request(self, microservice : str, resource : str, verb : str) -> list:
        """
        Extract the request parameters when executing the verb in the resource
        """

        return self.structure[microservice][resource][verb]["request"]
    
    def extract_verb_response(self, microservice : str, resource : str, verb : str) -> list:
        """
        Extract the response parameters when executing the verb in the resource
        """
        return self.structure[microservice][resource][verb]["response"] 
    
    def __repr__(self):
        return self.structure
