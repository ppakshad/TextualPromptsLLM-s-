# Prompt-Based LLMs for Software Vulnerability Detection

This repository presents a lightweight, structure-agnostic framework to evaluate the capability of Large Language Models (LLMs) in detecting software vulnerabilities directly from **raw source code**, without relying on structural representations such as AST, CFG, or DFG.

---

## System Architecture

![architecture](photo_5866124925276900285_y.jpg)

The proposed system consists of two main phases:

### 1. **Preprocessing Phase**
- Input datasets: 
  - `VDISC`: Annotated with CWE categories (e.g., CWE-119, CWE-476)
  - `CodeXGLUE`: Labeled with binary vulnerability classes
- Tasks:
  - Normalize code syntax
  - Convert CWE labels to binary form (`vulnerable` / `non-vulnerable`)
  - Tokenize and unify samples into structured JSON format
  - Output directory: `output_jsons/`

### 2. **Prompt-Based Evaluation Phase**
- Uses handcrafted prompts to simulate expert-level vulnerability reasoning
- Each function is analyzed by an LLM (e.g., GPT-4, Falcon, Gemini) via API
- The model predicts whether a function is vulnerable (1) or not (0)
- A final report is generated showing accuracy and misclassified samples

---

## Evaluated LLMs

The following Large Language Models were tested using our prompt-based vulnerability detection pipeline. Each model received identical prompts and code samples, and their accuracy was measured without any structural code input (e.g., no AST, CFG, or DFG):

| Model                     | Developer                           | License        | Accuracy (%) |
|---------------------------|-------------------------------------|----------------|--------------|
| **GPT-4o**                | OpenAI                              | Proprietary    | 43%          |
| **Falcon-180B-Chat**      | Technology Innovation Institute (TII) | Apache 2.0     | 42%          |
| **GEMINI-pro 1.0**        | Google Research                     | Proprietary    | 40%          |
| **Mistral-7B-Instruct-v0.2** | Mistral AI                        | Apache 2.0     | 38%          |
| **GPT-3.5**               | OpenAI                              | Proprietary    | 37%          |
| **Llama-3-8B**            | Nvidia                              | Open-source    | 27%          |

> All models were evaluated under identical zero-shot conditions using OpenAI-compatible or public APIs.

These results demonstrate that while LLMs can detect basic vulnerability patterns via textual reasoning alone, their accuracy remains limited without access to structural program representations.


---

## Prompt Design
To support accurate detection via natural language prompts, we developed six distinct prompt templates, each focusing on a common vulnerability type found in C/C++ code. These prompts contain a set of positive and negative examples to guide the model in binary classification (vulnerable: 1, non-vulnerable: 0):

Buffer Overflow: Identifies unsafe memory operations (e.g., strcpy, gets) versus secure patterns (e.g., strncpy, snprintf).

Use-After-Free: Flags cases where freed memory is accessed or modified after deallocation.

Integer Overflow: Detects arithmetic overflows, especially in memory allocations and multiplications.

Format String Vulnerability: Highlights insecure usage of uncontrolled format strings in functions like printf and fprintf.

Command Injection: Detects unsafe usage of system commands constructed from user input (e.g., system, execl).

Denial of Service (DoS/DDoS): Focuses on patterns that may lead to resource exhaustion, such as infinite loops, large unchecked allocations, or unbounded recursion.

These prompt designs help simulate expert vulnerability reasoning and assess the model’s robustness in identifying flaws in source code without access to intermediate representations.


---

---

## How to Run

1. Install dependencies:

```bash pip install openai tqdm```

2. Add your OpenAI API key to the script (if using gpt-4-turbo):
   
```API_KEY = "sk-..."  # Add your key in dataEvaluator.py```

3. Place preprocessed JSON dataset(s) inside the output_jsons/ directory


4. Run the evaluator:

 ```python dataEvaluator.py ```


