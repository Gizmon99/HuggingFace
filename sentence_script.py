import sys
from transformers import AutoModelForCausalLM, AutoTokenizer
checkpoint = "HuggingFaceTB/SmolLM2-1.7B-Instruct"

if len(sys.argv) == 2:
    mode = sys.argv[1]

device = "cpu" # "gpu" for GPU usage or "cpu" for CPU usage
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)

output_file = f"generated_output_{mode}.txt"


hehe = ["love", "meat", "food", "Canada", "asteroid"]
n = len(hehe)


new_lines = set()
for i in range(n):
    messages = [{"role": "user", "content": f"Can You generate a sentence with words 'cat' and {hehe[i]}?"}]
    input_text=tokenizer.apply_chat_template(messages, tokenize=False)
    inputs = tokenizer.encode(input_text, return_tensors="pt").to(device)
    outputs = model.generate(inputs, max_new_tokens=1000, temperature=0.2, top_p=0.9, do_sample=True)

    output_text = tokenizer.decode(outputs[0]).replace("\n", "")
    new_lines.add(output_text)

# combined_lines = existing_lines.union(new_lines)

with open(output_file, "w") as file:
    file.write("\n".join(new_lines))

print(f"Output appended to {output_file}")