import re, sys

if len(sys.argv) == 2:
    mode = sys.argv[1]

input_file = f"generated_output_{mode}.txt"
output_file = f"cleaned_output_{mode}.txt"


def clean_line(line):
    line = re.sub(r"<\|im_start\|>.*?<\|im_end\|>", "", line, count=2, flags=re.DOTALL)
    line = re.sub(r"<\|im_start\|>assistant", "", line)
    line = line.replace("<|im_end|>", "")
    line = line.strip()

    return line


with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        cleaned_line = clean_line(line)
        if cleaned_line:
            outfile.write(cleaned_line + "\n")
