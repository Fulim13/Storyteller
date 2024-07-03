import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# initialize tokenizer and model from pretrained GPT2 model from Huggingface
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2', pad_token_id=tokenizer.eos_token_id)

# sentence
sequence = "write a romantice story about a couple who met in a coffee shop."
# sequence = input("Enter a sentence: ")

# encoding sentence for model to process
inputs = tokenizer.encode(sequence, return_tensors='pt')

# generating text
outputs = model.generate(inputs, max_length=100000000, do_sample=True, num_beams=5, no_repeat_ngram_size=2, early_stopping=False)

# decoding text
text = tokenizer.decode(outputs[0], skip_special_tokens=True)
# printing output
print("\n")
print(text)

# https://medium.com/@majd.farah08/generating-text-with-gpt2-in-under-10-lines-of-code-5725a38ea685
# https://www.kaggle.com/code/tuckerarrants/text-generation-with-huggingface-gpt2