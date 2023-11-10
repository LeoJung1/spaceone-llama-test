from datasets import load_dataset
from transformers import LlamaTokenizer, LlamaForCausalLM, DataCollatorWithPadding, TrainingArguments, Trainer


def format_prompt(input, context, output):
    """
    Format of the prompt that will be inserted into Tokenizer
    """

    template = f"Input : {input} \n 
                Context : {context} \n, 
                Output : {output}"
    return template

# The 3 billion parameter model of llama address
model_path = "openlm-research/open_llama_3b_v2"

# Our Llama Tokenizer and our Llama Model
tokenizer = LlamaTokenizer.from_pretrained(model_path)
model = LlamaForCausalLM.from_pretrained(model_path)
print("BROUGHT THE MODEL IN\n")

def generate_prompt_to_token(datapoint):
    """
    Function that formats a single entry in the json file to a prompt 
    and convert it to a token in to a tensor
    """
    p = format_prompt(datapoint["input"],datapoint["context"], datapoint["output"])
    t = tokenizer(p, truncation=True, padding=False,return_tensors=None, max_length=100)
    return t


# Load and divide the datset into training and test sets
data = load_dataset("json", data_files="sql_data.jsonl")
train_val = data["train"].train_test_split(test_size=50, shuffle=True, seed=42)

# For each of the entry in both the training and test set, we want to convert them into a prompt format and tokenize them
train_data = train_val["train"].shuffle().map(generate_prompt_to_token, remove_columns=train_val["train"].column_names)
valid_data = train_val["test"].shuffle().map(generate_prompt_to_token, remove_columns=train_val["test"].column_names)

# applying data processing like padding to build batches for batch jobs
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
training_args = TrainingArguments("test-trainer", use_mps_device=True)


print("TRAINING...\n")
trainer = Trainer(model, 
                  training_args,
                  train_dataset=train_data, 
                  eval_dataset=valid_data,
                  data_collator=data_collator,
                  tokenizer=tokenizer,
                )



def main():
    trainer.train()

if __name__ == "__main__":
    print("Training...\n")
    main()
    print("Training Complete!")

















# DATA_PATH = Path("./source")

# def get_data_path(data_dir):
#     return DATA_PATH / data_dir / "data_sql_short.jsonl"


# def load_data_sql(data_dir: str = "data_sql"):
#     from datasets import load_dataset

#     dataset = load_dataset("b-mc2/sql-create-context")

#     dataset_splits = {"train": dataset["train"]}
#     output_path = get_data_path(data_dir)

#     output_path.parent.mkdir(parents=True, exist_ok=True)

#     # print(dataset_splits.items())
#     count = 0
#     for key, ds in dataset_splits.items():
#         with open(output_path, "w") as f:
#             for item in ds:
#                 if count == 10:
#                     break
#                 newitem = {
#                     "input": item["question"],
#                     "context": item["context"],
#                     "output": item["answer"],
#                 }
#                 f.write(json.dumps(newitem) + "\n")
#                 count += 1
# load_data_sql()


# data_path = get_data_path("data_sql").as_posix()
# data = load_dataset("json", data_files=data_path)
# print(data)

# def generate_prompt(input, context, answer):
#     return f" Input : {input} \n Context : {context} \nOutput : {answer}"


# def generate_prompt_tokenize(datapoint):
#     p = generate_prompt(datapoint["input"], datapoint["context"], datapoint["output"])


# 3 Billion Parameters


# tokenizer = LlamaTokenizer.from_pretrained(model_path)
# model = LlamaForCausalLM.from_pretrained(
#     model_path, 
#     torch_dtype=torch.float16, 
#     device_map="auto"
# )

# Train the Data

# def template()


# prompt = "Q: What is the largest animal? \nA:"
# input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to("mps")

# generation_output = model.generate(
#     input_ids=input_ids, max_new_tokens=32
# )

# print(tokenizer.decode(generation_output[0]))


