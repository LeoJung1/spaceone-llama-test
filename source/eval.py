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

eval_prompt = f"""<<SYS>>
You are a helpful SpaceOne Assistant. Your job is to answer questions that the user asks about SpaceOne. Try to answer in a SpaceOne manner as best as possible.
If a question doesn't make sense, don't answer ambiguously but you can ask again for more details.
<</SYS>>

### Task Name: search_resources

[INST]
### Instruction: List all the existing resources in the SpaceOne <Identity> microservice.
### Input: <No Input>
[/INST]

### Output: 
"""

model_input = tokenizer(eval_prompt, return_tensors="pt").to("cuda")

model.eval()
with torch.no_grad():
    print(tokenizer.decode(model.generate(**model_input, max_new_tokens=100)[0], skip_special_tokens=True))