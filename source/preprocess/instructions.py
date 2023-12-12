def microservice_instruct():
    """
    Instructions for the Microservice
    """
    instruction_1 = "What microservices exist in the SpaceOne?"
    instruction_2 = "Give me all the microservices in SpaceOne"
    instruction_3 = "What specific microservicse form part of SpaceOne's architecture?"
    instruction_4 = "Can you list the microservices present in the SpaceOne platform?"
    instruction_5 = "Enumerate the microservices within the SpaceOne platform"
    instruction_6 = "What is the roster of microservices within the SpaceOne platform?"
    instruction_7 = "Can you detail the microservices that make up the SpaceOne platform?"
    return {"inst_1" : instruction_1, "inst_2" : instruction_2, "inst_3" : instruction_3, "inst_4" : instruction_4, "inst_5" : instruction_5, "inst_6" : instruction_6, "inst_7" : instruction_7}

def resource_instruct(microservice):
    """
    Instructions for the Resource
    """
    instruction_1 = f"What resources are in {microservice} microservice?"
    instruction_2 = f"List all the resources that are existing in the inputted microservice"
    instruction_3 = f"In the {microservice} microservice, what resources are there?"
    instruction_4 = f"Name all the resources existing in the {microservice} microservice"
    instruction_5 = f"Show me all the resources that are existing in the following microservice"
    instruction_6 = f"Within the {microservice}, what resources are present?"
    instruction_7 = f"What resources constitute the {microservice} microservice?"
    return {"inst_1" : instruction_1, "inst_2" : instruction_2, "inst_3" : instruction_3, "inst_4" : instruction_4, "inst_5" : instruction_5, "inst_6" : instruction_6, "inst_7" : instruction_7}

def verb_instruct(resource):
    """
    Instructions for the Verbs
    """
    instruction_1 = f"What are the executable verbs existing in the {resource} resource?"
    instruction_2 = f"I want to know the possible executable verbs of the following resource"
    instruction_3 = f"What verbs can I use for the {resource} resource?"
    instruction_4 = f"List all the verbs that I can utilize for the {resource} resource"
    instruction_5 = f"Outline all the verbs that are existent in the following resource"
    instruction_6 = f"Name all verbs that could be used for {resource}"
    instruction_7 = f"What verb functions can be used for the {resource} resource?"
    return {"inst_1" : instruction_1, "inst_2" : instruction_2, "inst_3" : instruction_3, "inst_4" : instruction_4, "inst_5" : instruction_5, "inst_6" : instruction_6, "inst_7" : instruction_7}


def parameter_instruct(resource, verb):
    """
    Instructions for the parameters
    """
    #Instruction that require input : Inst_2, Inst_5
    instruction_1 = f"""Show me the parameters required to execute "{verb}" in {resource} resource"""
    instruction_2 = f"""What parameters are needed to execute the following verb in the resource?"""
    instruction_3 = f"""I want to execute "{verb}" in the {resource} resource. What are the required parameters?"""
    instruction_4 = f"""What schemas do I need to execute the "{verb}" verb for the {resource} resource?"""
    instruction_5 = f"""List out the required parameters need for the execution of the following verb in the resource"""

    # Instruction that require input : Inst_7, Inst_10
    instruction_6 = f"""Show me the resulting parameters when I execute "{verb}" in the {resource} resource"""
    instruction_7 = f"""What do I get when I execute the following verb in the resource?"""
    instruction_8 = f"""What is the response that I get when I execute "{verb}" in {resource} resource?"""
    instruction_9 = f"""What kind of variables will I get as a response when I use "{verb}" in {resource}? """
    instruction_10 = f"""For executing the following verb in its resource, what is the response that I will get?"""
    return {"inst_1" : instruction_1, "inst_2" : instruction_2, "inst_3" : instruction_3, "inst4" : instruction_4, "inst_5" : instruction_5, 
            "inst_6" : instruction_6, "inst_7": instruction_7, "inst_8" : instruction_8, "inst_9" : instruction_9, "inst_10" : instruction_10}

