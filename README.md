# PersianMCQ-Instruct

**PersianMCQ-Instruct** is a comprehensive resource that includes datasets and advanced models for generating multiple-choice questions (MCQs) in standard Iranian Persian—a low-resource language spoken by over 80 million people. This project provides valuable tools for researchers and educators, aiming to enhance Persian-language educational technology.

## Overview

We present three state-of-the-art models for Persian MCQ generation:

- **PMCQ-Gemma2-9b**
- **PMCQ-Llama3.1-8b**
- **PMCQ-Mistral-7B**

Inspired by the Agent Instruct framework and **GPT-4**, we created a dataset by curating over 4,000 unique Persian Wikipedia pages and generating three MCQs per page, resulting in a total of over 12,000 questions. Both human evaluations and model fine-tuning were conducted to ensure dataset quality, showing substantial performance improvements in Persian MCQ generation.

## Features

- **Multiple Pre-trained Models**: Choose from three advanced models fine-tuned for Persian MCQ generation.
- **Customizable Generation Parameters**: Adjust settings like temperature to control the creativity of the generated content.
- **Command-Line Interface**: Easily run the script with different parameters through a simple CLI.
- **Supports Persian Language**: Tailored for standard Iranian Persian, catering to a significant linguistic community.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Input File Format](#input-file-format)
  - [Output](#output)
- [Notes](#notes)
- [Building the `requirements.txt` File](#building-the-requirementstxt-file)
- [License](#license)

## Requirements

- **Python**:  Python 3.7 or higher
- **Hardware**:
  - CUDA-compatible GPU (recommended for faster processing and to handle larger models)
  - At least 16 GB of RAM (more may be required depending on the model)
- **Dependencies**:
  - See [`requirements.txt`](#building-the-requirementstxt-file) for a list of Python packages needed.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/Persian_MCQ.git
   cd Persian_MCQ
   ```

2. **Create a Virtual Environment (Recommended)**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the Required Packages**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Download the Models**:

   The models will be automatically downloaded the first time you run the script. Ensure you have a stable internet connection.

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
python generate_persian_mcq.py \
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

## Building the `requirements.txt` File

To ensure all necessary dependencies are installed, a `requirements.txt` file is provided. Below are instructions on how to create or update it.

### Sample `requirements.txt`:

```text
pandas==2.2.3
transformers==4.44.0.dev0
```

### Steps to Create or Update `requirements.txt`:

1. **Manual Creation**:

   - Create a file named `requirements.txt`.
   - List all the required packages with their versions.

2. **Automatic Generation**:

   If you've installed packages in your virtual environment, you can generate the file automatically:

   ```bash
   pip freeze > requirements.txt
   ```

   **Note**: This may include more packages than necessary. It's a good practice to review and edit the file to include only the required dependencies.

### Installing Dependencies Using `requirements.txt`:

```bash
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License.

---

We hope that **PersianMCQ-Instruct** serves as a valuable resource in advancing educational technology and research for the Persian language community.

For any questions or contributions, please open an issue or submit a pull request.

---

# Reference

This project is based on the research presented in the paper:

> **Title**: PersianMCQ-Instruct: A Resource for Persian Multiple Choice Question Generation
>
> **Abstract**:
>
> We present **PersianMCQ-Instruct**, a comprehensive resource comprising a dataset and advanced models for generating multiple-choice questions (MCQs) in standard Iranian Persian, a low-resource language spoken by over 80 million people. This resource includes three state-of-the-art models for Persian MCQ generation: **PMCQ-Gemma2-9b**, **PMCQ-Llama3.1-8b**, and **PMCQ-Mistral-7B**. Inspired by the Agent Instruct framework and **GPT-4**, we created the dataset by curating over 4,000 unique Persian Wikipedia pages, generating three MCQs per page for a total of over 12,000 questions.
>
> To ensure the quality of the dataset, we conducted both human evaluations and model fine-tuning, which showed substantial performance improvements in the Persian MCQ generation. The dataset and models are publicly available, providing valuable tools for researchers and educators, with a particular impact on enhancing Persian-language educational technology.

---

**Note**: The models and datasets are intended for research and educational purposes. Always ensure compliance with local regulations and ethical guidelines when using AI models and data.
