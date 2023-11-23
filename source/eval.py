import torch

from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base_model = "codellama/CodeLlama-7b-hf"
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    load_in_8bit=True,
    torch_dtype=torch.float16,
    device_map="auto",
)

output_dir = "sql-code-llama"
tokenizer = AutoTokenizer.from_pretrained("codellama/CodeLlama-7b-hf")
model = PeftModel.from_pretrained(model, output_dir)

eval_prompt = """You are a powerful cloudforet API model. Your job is to understand the struct of Cloudforet API.
Given the question, give me the response as the command that will be used for the CLI.

### Question : Show me all the resources in the inventory service

### Response:
"""

model_input = tokenizer(eval_prompt, return_tensors="pt").to("cuda")

model.eval()
with torch.no_grad():
    print(tokenizer.decode(model.generate(**model_input, max_new_tokens=100)[0], skip_special_tokens=True))