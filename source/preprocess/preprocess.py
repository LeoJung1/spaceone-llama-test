import json

from datasets import load_dataset


def preprocessing():
    """
    Preprocess the loaded dataset from huggingface and format them into a newly created JSON file.
    """
    data = load_dataset("b-mc2/sql-create-context")
    training_dataset = {"train" : data["train"]}

    file = "sql_data.jsonl"    
    with open(file,"w") as f:
        line_count = 0
        threshold = 100
        for row in training_dataset["train"]:
            # if line_count == threshold:
            #     break
            line = {"input" : row["question"],
                    "context" : row["context"],
                    "output" : row["answer"]}
            f.write(json.dumps(line) + "\n")
            # line_count += 1

preprocessing()