from transformers import AutoModelForCausalLM, AutoTokenizer
import argparse
import pandas as pd

# Prompt to be used
PROMPT = '''As an Educational Assistant, create a multiple-choice question in Persian from a given text, ensuring that the question has one correct answer and three plausible distractors. Follow these guidelines:
1- Identify key concepts and details.
2- Use clear, concise, grammatically correct Persian.
3- Correct answers must be directly from the text.
4- Provide a question in the list format as follows:
Question ? الف. Correct answer (پاسخ صحیح) ب. Incorrect answer (پاسخ غلط) ج. Incorrect answer (پاسخ غلط) د. Incorrect answer (پاسخ غلط)''' + '\n\nText: '

# Model-specific configurations
MODEL_CONFIGS = {
    "PMCQ-Gemma2-9b": {
        "path": "Kamyar-zeinalipour/PMCQ-Gemma2-9b",
        "format_row": lambda row: f'<bos><start_of_turn>user\n{PROMPT}{row["text"]}\n<start_of_turn>model\n',
        "extract_text": lambda text: text.split('<start_of_turn>model\n')[1].split('<end_of_turn>')[0] if '<start_of_turn>model\n' in text and '<end_of_turn>' in text else None
    },
    "PMCQ-Llama3.1-8b": {
        "path": "Kamyar-zeinalipour/PMCQ-Llama3.1-8b",
        "format_row": lambda row: f'<|begin_of_text|><|start_header_id|>system<|end_header_id|>\nYou are helpful assistant\n<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{PROMPT}{row["text"]} <|eot_id|><|start_header_id|>assistant<|end_header_id|>',
        "extract_text": lambda text: text.split('<|end_header_id|>\n\n')[2].split('<|end_of_text|>')[0] if text.count('<|end_header_id|>\n\n') > 1 else None
    },
    "PMCQ-Mistral-7B": {
        "path": "Kamyar-zeinalipour/PMCQ-Mistral-7B",
        "format_row": lambda row: f'<s>[INST] {PROMPT}{row["text"]} [/INST] ',
        "extract_text": lambda text: text.split('[/INST]')[1].split('</s>')[0] if '[/INST]' in text and '</s>' in text else None
    }
}

def get_code_completion(text, model, tokenizer, temperature):
    """Generates code completion for the given text using the model."""
    model.eval()
    input_ids = tokenizer(text, return_tensors="pt").input_ids.cuda()
    outputs = model.generate(
        input_ids=input_ids,
        max_new_tokens=1024,
        temperature=temperature,
        top_k=50,
        top_p=0.95,
        do_sample=True,
        repetition_penalty=1.1,
        eos_token_id=tokenizer.eos_token_id,
    )
    return tokenizer.batch_decode(outputs, skip_special_tokens=False)[0]

def main(args):
    # Retrieve model configuration based on the specified model name
    model_config = MODEL_CONFIGS.get(args.model_name)
    if not model_config:
        raise ValueError(f"Unsupported model name: {args.model_name}")

    # Load model and tokenizer
    print(f"Starting to load the model {args.model_name} into memory")
    model = AutoModelForCausalLM.from_pretrained(model_config["path"])
    tokenizer = AutoTokenizer.from_pretrained(model_config["path"])

    if not hasattr(model, "hf_device_map"):
        model.cuda()

    print(f"Successfully loaded the model {args.model_name} into memory")

    # Read input CSV
    df = pd.read_csv(args.input_file)

    # Initialize list to store outputs
    outputs = []

    for index, row in df.iterrows():
        # Apply the formatting template to the 'text' column
        prompt = model_config["format_row"](row)

        try:
            # Get generated response
            response = get_code_completion(prompt, model, tokenizer, args.temperature)
            generated_text = model_config["extract_text"](response)
            print('Index:', index)
            print('Input text:', row['text'])
            print('Generated Persian MCQ:  ', generated_text)

            outputs.append({
                'text': row['text'],
                'Generated Persian MCQ': generated_text
            })

        except Exception as e:
            print(f"Error processing row: {row['text']}. Error: {e}")

    # Save results to CSV
    output_df = pd.DataFrame(outputs)
    output_df.to_csv(args.output_file, index=False)
    print(f"Generated output saved to {args.output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate text using a language model.')
    parser.add_argument('--model-name', type=str, required=True, help='Pretrained model name. Use "PMCQ-Gemma2-9b", "PMCQ-Llama3.1-8b", or "PMCQ-Mistral-7B"')
    parser.add_argument('--input-file', type=str, required=True, help='Path to the input CSV file')
    parser.add_argument('--output-file', type=str, default= 'output.csv', help='Path to save the output CSV file')
    parser.add_argument('--temperature', type=float, default=0.1, help='Temperature for text generation')
    
    args = parser.parse_args()
    main(args)
