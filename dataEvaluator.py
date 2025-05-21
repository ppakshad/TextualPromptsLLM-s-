import h5py
import re
import json
import os
import time
from tqdm import tqdm
from openai import OpenAI

output_dir = "PATH...."  # Directory where JSON files are saved
API_KEY = "API KEY!!..." # OpenAI API Key


client = OpenAI(api_key=API_KEY)

def get_first_json_file():
    json_files = sorted([f for f in os.listdir(output_dir) if f.endswith(".json")])
    if json_files:
        return os.path.join(output_dir, json_files[0])  # Get the first generated JSON file
    return None

def read_first_100_functions(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
        functions = data.get("functions", [])[:10]  # Get the first 100 functions
    return functions

def extract_answer(response):
    if response.strip():
        match = re.search(r"(0|1)", response)
        if match:
            return int(match.group(1))
    return None

# Function to send function body to llm model for classification
def ask_llm(function_body, max_retries=5):
    prompt = f""""""   # PROMPT DEFENITOON !
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="", 
                messages=[
                    {"role": "system", "content": "You are a security expert analyzing source code for vulnerabilities."},
                    {"role": "user", "content": prompt},
                ]
            )
            if response.choices:
                result = extract_answer(response.choices[0].message.content)
                if result is not None:
                    return result
                else:
                    print("Incorrect response format detected. Retrying...")
        except Exception as e:
            print(f"Error: {e}. Retrying in {2 ** attempt} seconds.")
            time.sleep(2 ** attempt)
    return None

# Function to evaluate Model results
def evaluate_gpt_results():
    json_file = get_first_json_file()
    if not json_file:
        print("No JSON files found in the directory.")
        return

    print(f"\n Using first JSON file for evaluation: {json_file}")
    
    functions = read_first_100_functions(json_file)
    
    correct_predictions = 0
    incorrect_predictions = []

    with tqdm(total=len(functions), desc="Processing Model Requests") as progress_bar:
        for func in functions:
            function_body = func["functionBody"]
            function_signature = func["signature"]  # signature
            true_status = func["status"]  # Ground truth (0 or 1)

            gpt_status = ask_llm(function_body)
            
            if gpt_status == true_status:
                correct_predictions += 1
            else:
                incorrect_predictions.append({
                    "signature": function_signature,  
                    "true_status": true_status,
                    "gpt_status": gpt_status
                })

            accuracy_rate = correct_predictions / (progress_bar.n + 1) * 100
            progress_bar.set_postfix_str(f"Accuracy: {accuracy_rate:.2f}%")
            progress_bar.update(1)

    print(f"\n **Final Accuracy**: {correct_predictions / len(functions) * 100:.2f}%")    
    
    if incorrect_predictions:
        print("\n Incorrect Predictions (List of Function Signatures):")
        for item in incorrect_predictions:
            print(f"- {item['signature']}") 


# Main execution
if __name__ == "__main__":
    evaluate_gpt_results()