import json
import random
from instructions import microservice_instruct, resource_instruct, verb_instruct, parameter_instruct
from spaceone_structure import SpaceoneStructure

def create_line(task_name, instruction, instances):
    line = {
        "task name" : task_name,
        "instruction" : instruction,
        "instances" : instances
    }
    return line

def main():
    output_file = "seed_task_data.jsonl"
    seed_task_test_file = "seed_task_test.jsonl"
    spaceone_structure = SpaceoneStructure()
    json_result = []
    microservice_instructions = microservice_instruct()
    for instruction in microservice_instructions:
        micro_instance = [{"input" : "<No Input>", "output" : ", ".join(spaceone_structure.extract_microservice())}]
        line = create_line("search_microservice", microservice_instructions[instruction], micro_instance)
        json_result.append(line)
        
    for microservice in spaceone_structure.structure:
        for resource in spaceone_structure.structure[microservice]:
            resource_instruction = resource_instruct(microservice)
            output = ", ".join(spaceone_structure.extract_resources(microservice))
            # Create instruction for resources
            for instruction in resource_instruction:
                if instruction == "inst_2" or instruction == "inst_5":
                    res_instances = [{"input" : microservice, "output": output}]
                else:
                    res_instances = [{"input" : "<No Input>", "output":output}]
                resource_line = create_line("search_resource", resource_instruction[instruction], res_instances)
                json_result.append(resource_line)

            for verb in spaceone_structure.structure[microservice][resource]:

                verb_instruction = verb_instruct(resource)
                verb_output = ",".join(spaceone_structure.extract_verbs(microservice, resource))
                for instruction in verb_instruction:
                    if instruction == "inst_2" or instruction == "inst_5":
                        v_instances = [{"input" : resource, "output": verb_output}]
                    else:
                        v_instances = [{"input": "<No Input>", "output": verb_output}]
                    verb_line = create_line("search_verb", verb_instruction[instruction], v_instances)
                    json_result.append(verb_line)


                parameter_instruction = parameter_instruct(resource, verb)
                parameter_request = ", ".join(spaceone_structure.extract_verb_request(microservice, resource, verb))
                parameter_response = ", ".join(spaceone_structure.extract_verb_response(microservice, resource, verb))
                for instruction in parameter_instruction:
                    if instruction == "inst_2" or instruction == "inst_5":
                        par_instances = [{"input" : f"Resource : {resource}, Verb : {verb}", "output": parameter_request}]
                    elif instruction in ["inst_1", "inst_3", "inst_4"]:
                        par_instances = [{"input" : "<No Input>", "output" : parameter_request}]
                    elif instruction == "inst_6" or instruction == "inst_10":
                        par_instances = [{"input" : f"Resource : {resource}, Verb : {verb}", "output" : parameter_response}]
                    else:
                        par_instances = [{"input" : "<No Input>", "output": parameter_response}]
                    param_line = create_line("search_parameters", parameter_instruction[instruction], par_instances)
                    json_result.append(param_line)
                    
                        
                
    with open(output_file, "w") as f:
        random.shuffle(json_result)
        json.dump(json_result, f, indent=4)

    selected_items = []
    for i in json_result:
        selected_item = random.choice(json_result) if random.random() < 0.1 else None
        if selected_item:
            selected_items.append(selected_item)

    with open(seed_task_test_file, "w") as f:
        json.dump(selected_items, f)
        

if __name__ == "__main__":
    main()
