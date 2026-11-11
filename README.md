# PersianMCQ-Instruct

**Multiple-choice question generation in Persian**

[![Paper](https://img.shields.io/badge/LoResLM_2025-paper-b31b1b)](https://aclanthology.org/2025.loreslm-1.27/)
[![Dataset](https://img.shields.io/badge/%F0%9F%A4%97_Dataset-PersianMCQ--instruct-yellow)](https://huggingface.co/datasets/Kamyar-zeinalipour/PersianMCQ-instruct)
[![Models](https://img.shields.io/badge/%F0%9F%A4%97_Collection-3_models-orange)](https://huggingface.co/collections/Kamyar-zeinalipour/persianmcq-instruct-loreslm-2025-6af481273fff746c25e21f62)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE.txt)

PersianMCQ-Instruct is a dataset and a set of fine-tuned models for generating multiple-choice
questions (MCQs) in standard Iranian Persian. Following the AgentInstruct approach, GPT-4o
generated and refined three MCQs for each of more than 4,000 Persian Wikipedia pages, giving
12,476 questions. Fine-tuning Gemma-2, Llama-3.1 and Mistral on this data sharply improves the
questions they write. This repository accompanies the paper
[*PersianMCQ-Instruct: A Comprehensive Resource for Generating Multiple-Choice Questions in
Persian*](https://aclanthology.org/2025.loreslm-1.27/) (LoResLM 2025).

| Resource | |
|---|---|
| [PersianMCQ-instruct](https://huggingface.co/datasets/Kamyar-zeinalipour/PersianMCQ-instruct) | The dataset: Persian passages with generated and refined MCQs |
| [PMCQ-Gemma2-9b](https://huggingface.co/Kamyar-zeinalipour/PMCQ-Gemma2-9b) | Gemma-2-9B-it fine-tuned with LoRA |
| [PMCQ-Llama3.1-8b](https://huggingface.co/Kamyar-zeinalipour/PMCQ-Llama3.1-8b) | Llama-3.1-8B-Instruct fine-tuned with LoRA |
| [PMCQ-Mistral-7B](https://huggingface.co/Kamyar-zeinalipour/PMCQ-Mistral-7B) | Mistral-7B-Instruct-v0.3 fine-tuned with LoRA |
| [HumanAnnotation-UI-PMCQ](https://github.com/KamyarZeinalipour/HumanAnnotation-UI-PMCQ) | Human-evaluation protocol |

## Results

Human ratings of 200 generated questions per model (A = 5 … E = 1; Table 3 of the paper):

| Model | Base | Fine-tuned (PMCQ) |
|---|---:|---:|
| Gemma-2-9B-it | 2.72 | **2.78** |
| Llama-3.1-8B-Instruct | 3.31 | **4.51** |
| Mistral-7B-Instruct-v0.3 | 1.30 | **4.32** |
| PersianMCQ-Instruct (GPT-4o reference) | | 4.75 |

BERTScore F1 between generated and reference questions (Table 2): Gemma 0.888 → **0.903**,
Llama 0.881 → **0.905**, Mistral 0.874 → **0.904**.

## Installation

```bash
git clone https://github.com/KamyarZeinalipour/Persian_MCQ.git
cd Persian_MCQ
pip install -r requirements.txt
huggingface-cli login   # the base models are gated: accept their licenses on Hugging Face first
```

## Usage

The script can be executed from the command line with various arguments to customize its behavior.

**Basic Command Structure**:

```bash
python main.py --model-name <MODEL_NAME> --input-file <INPUT_CSV> --output-file <OUTPUT_CSV> [--temperature <TEMPERATURE>]
```

### Arguments

- `--model-name`: **(Required)** Name of the pre-trained model to use.
  - Options: `"PMCQ-Gemma2-9b"`, `"PMCQ-Llama3.1-8b"`, `"PMCQ-Mistral-7B"`
- `--input-file`: **(Required)** Path to the input CSV file containing the prompts.
- `--output-file`: **(Required)** Path where the output CSV file will be saved.
- `--temperature`: (Optional) Controls the randomness of the generation.
  - Default is `0.1`. Higher values like `0.8` will make the output more random, while lower values like `0.2` will make it more deterministic.

### Example Command

```bash
python main.py \
  --model-name PMCQ-Gemma2-9b \
  --input-file data/input_prompts.csv \
  --output-file data/generated_mcqs.csv \
  --temperature 0.7
```

### Input File Format

The input CSV file should contain at least one column named `text`, which includes the prompts for MCQ generation.

**Sample `input_prompts.csv`**:

| text                                      |
|-------------------------------------------|
| این یک نمونه سوال برای تولید گزینه‌ها است. |

### Output

The script generates a CSV file containing the original prompts and the generated MCQs.

**Sample `generated_mcqs.csv`**:

| text                                      | Generated Persian MCQ                          |
|-------------------------------------------|------------------------------------------------|
| این یک نمونه سوال برای تولید گزینه‌ها است. | **(Generated MCQ text here)**                  |

## Notes

- **GPU Memory**: Ensure your GPU has enough memory to load and run the models. Models like `PMCQ-Gemma2-9b` are resource-intensive.
- **Model Loading Time**: Loading large models may take several minutes. Please be patient.
- **Internet Connection**: A stable internet connection is required to download models from Hugging Face's model hub if they are not present locally.
- **Customization**: Feel free to adjust parameters like `max_new_tokens` in the script for finer control over the output length.

## Training

```bash
pip install -r requirements-train.txt
scripts/train_llama3.sh      # also train_gemma2.sh, train_mistral.sh
```

The models were fine-tuned on the `Persian_MCQ_DB_*` datasets (the PersianMCQ-Instruct questions in
each model's chat format; 12,000 training and 476 test items) with LoRA r = 16, α = 32, dropout 0.1
on all attention and MLP projections plus the embeddings and LM head; 3 epochs, AdamW, learning
rate 1e-4 with cosine decay, weight decay 1e-4; 4 sequences per GPU × 4 accumulation steps, up to
3,500 tokens; bf16, DeepSpeed, Flash Attention 2, seed 100.

## Citation

```bibtex
@inproceedings{zeinalipour-etal-2025-persianmcq,
    title = "{P}ersian{MCQ}-Instruct: A Comprehensive Resource for Generating Multiple-Choice Questions in {P}ersian",
    author = "Zeinalipour, Kamyar  and
      Jamshidi, Neda  and
      Akbari, Fahimeh  and
      Maggini, Marco  and
      Bianchini, Monica  and
      Gori, Marco",
    editor = "Hettiarachchi, Hansi  and
      Ranasinghe, Tharindu  and
      Rayson, Paul  and
      Mitkov, Ruslan  and
      Gaber, Mohamed  and
      Premasiri, Damith  and
      Tan, Fiona Anting  and
      Uyangodage, Lasitha",
    booktitle = "Proceedings of the First Workshop on Language Models for Low-Resource Languages",
    month = jan,
    year = "2025",
    address = "Abu Dhabi, United Arab Emirates",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.loreslm-1.27/",
    pages = "344--372"
}
```

## License

Code: [MIT](LICENSE.txt). The models follow the licenses of their base models.
