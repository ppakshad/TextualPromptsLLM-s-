import h5py
import re
import json
import os
import time
from tqdm import tqdm  

file_path_hdf5 = "VDISC_train.hdf5" #VDUSC DATASET
file_path_jsonl = "CodeXGLUE/train.jsonl" #CodeXGLUE DATA SET
output_dir = "output_jsons" 
os.makedirs(output_dir, exist_ok=True)  

def extract_function_signature(function_body): #extract function signature
    match = re.search(r"^\s*(?:\w+\s+)*(\w+\s*\(.*?\))", function_body, re.DOTALL | re.MULTILINE)
    return match.group(1) if match else "Unknown_Function()"

def process_hdf5(data_list):
    with h5py.File(file_path_hdf5, "r") as file:
        function_bodies = file["functionSource"][:] 
        cwe_keys = ["CWE-119", "CWE-120", "CWE-469", "CWE-476", "CWE-other"]
        cwe_labels = {cwe: file[cwe][:] for cwe in cwe_keys}
        total_functions = len(function_bodies)  

        print("\nProcessing HDF5 dataset...")
        for i in tqdm(range(total_functions), desc="HDF5 Progress", unit="func"):  
            function_body = function_bodies[i].decode("utf-8").strip()
            function_signature = extract_function_signature(function_body)
            is_vulnerable = any(cwe_labels[cwe][i] for cwe in cwe_keys)
            vulnerability_status = 1 if is_vulnerable else 0 

            data_list.append({
                "signature": function_signature,
                "functionBody": function_body,
                "status": vulnerability_status
            })

def process_jsonl(data_list):
    with open(file_path_jsonl, "r", encoding="utf-8") as file:
        lines = file.readlines() 
        total_functions = len(lines)

        print("\nProcessing JSONL dataset...")
        for i, line in enumerate(tqdm(lines, desc="JSONL Progress", unit="func")):  
            data = json.loads(line.strip())
            function_body = data.get("func", "").strip()
            function_signature = extract_function_signature(function_body)
            vulnerability_status = 1 if data.get("target", 0) == 1 else 0  # 1 = Vulnerable, 0 = Non-Vulnerable
            data_list.append({
                "signature": function_signature,
                "functionBody": function_body,
                "status": vulnerability_status
            })

def save_in_chunks(data_list, chunk_size=100000):
    total_files = (len(data_list) // chunk_size) + (1 if len(data_list) % chunk_size else 0)
    
    for i in range(total_files):
        chunk = data_list[i * chunk_size: (i + 1) * chunk_size]
        file_name = f"JsonDataset_{i+1:02d}.json"
        file_path = os.path.join(output_dir, file_name)

        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump({"functions": chunk}, json_file, indent=4, ensure_ascii=False)

        print(f" Saved {len(chunk)} functions to {file_path}")

def wait_for_json_and_count():
    print("\nWaiting for JSON files to be generated...")
    time.sleep(2) 

    total_functions = 0
    vulnerable_functions = 0
    non_vulnerable_functions = 0

    for file_name in os.listdir(output_dir):
        if file_name.endswith(".json"):
            with open(os.path.join(output_dir, file_name), "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
                functions = data.get("functions", [])
                total_functions += len(functions)
                vulnerable_functions += sum(1 for func in functions if func["status"] == 1)
                non_vulnerable_functions += sum(1 for func in functions if func["status"] == 0)

    print(f"\n **Function Statistics**")
    print(f"Total Functions in JSON Files: {total_functions}")
    print(f"Vulnerable Functions: {vulnerable_functions}")
    print(f"Non-Vulnerable Functions: {non_vulnerable_functions}")

if __name__ == "__main__":
    all_data = []  

    process_hdf5(all_data)  
    process_jsonl(all_data)  
    save_in_chunks(all_data, chunk_size=100000)
    wait_for_json_and_count()