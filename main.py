import os
import time
from datetime import datetime
from openai import OpenAI
import pandas as pd
import json

# Initialize OpenAI client
OPENAI_API_KEY = "your-api-key-here"
client = OpenAI(api_key=OPENAI_API_KEY)
    
# Path constants
PAPERS_DIR = os.path.join(os.path.dirname(__file__), "papers")

SETTINGS = {
    "model": "gpt-4.1-mini",
    "temperature": 1e-12,
    "top_p": 1
}

def upload_papers():
    """Upload all files in the 'papers' folder to OpenAI storage."""
    uploaded_files = {}
    local_files = [f for f in os.listdir(PAPERS_DIR) if os.path.isfile(os.path.join(PAPERS_DIR, f))]
    # local_files = local_files[:1] # Limit to first file for testing

    # Fetch existing files from OpenAI storage
    existing_files = {f.filename: f.id for f in client.files.list().data}

    # Upload missing files
    for filename in local_files:
        if filename not in existing_files:
            file_path = os.path.join(PAPERS_DIR, filename)
            print(f"Uploading: {filename} ...")
            with open(file_path, "rb") as f:
                file_obj = client.files.create(
                    file=f,
                    purpose="assistants"
                )
            uploaded_files[filename] = file_obj.id
        else:
            uploaded_files[filename] = existing_files[filename]

    # Verify all are in storage
    missing = [f for f in local_files if f not in uploaded_files]
    if missing:
        raise RuntimeError(f"The following files are missing in OpenAI storage: {missing}")

    print("All papers uploaded and verified.")
    return uploaded_files


def prompt(system_prompt_path: str, file_id: str, title: str, temperature: float = 1, top_p: float = 1, model: str = "gpt-4.1-mini"):
    """Send a prompt to the OpenAI responses endpoint with the given file and paper title."""
    response = client.responses.create(
        model= model,
        temperature= temperature,
        top_p= top_p,
        input=[
            {
                "role": "system",
                "content": open(system_prompt_path, "r").read()
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": f"Analyze the paper '{title}, see attached'."},
                    {"type": "input_file", "file_id": file_id}
                ]
            }
        ],
        text={
            "format": {"type": "text"}
        },
        max_output_tokens=2048
    )

    result_text = response.output[0].content[0].text.strip()

    # Parse result text as JSON
    try:
        parsed = json.loads(result_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse response text as JSON: {result_text}, error: {e}")

    return parsed

if __name__ == "__main__":
    # Step 1: Upload all papers
    uploaded = upload_papers()

    # Select mode
    c = input("Relevance (r) or extract (e) mode? [r/e]: ").strip().lower()

    if c == "r":
        system_prompt_path = os.path.join(os.path.dirname(__file__), "system_prompts", "relevance_check.md")
        results_file = os.path.join(os.path.dirname(__file__), "results_relevance.xlsx")
    elif c == "e":
        system_prompt_path = os.path.join(os.path.dirname(__file__), "system_prompts", "extract_information.md")
        results_file = os.path.join(os.path.dirname(__file__), "results_extract.xlsx")
    else:
        raise ValueError("Invalid mode selected. Choose 'r' or 'e'.")

    # Step 2: Iterate and send prompt for each paper
    for filename, file_id in uploaded.items():
        title = os.path.splitext(filename)[0]
        print(f"\nProcessing '{title}' ...")
        
        result = prompt(system_prompt_path=system_prompt_path, file_id=file_id, title=title, temperature=SETTINGS["temperature"], top_p=SETTINGS["top_p"], model=SETTINGS["model"])
        
        # Check if id in result is the same as id of file, sanity check
        if "id" not in result or result["id"] != int(filename.split(" - ")[0]):
            raise ValueError(f"Result ID mismatch or missing. Expected: {file_id}, Got: {result.get('id')}")

        # Add timestamp
        result["timestamp"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # Add settings info
        result["settings"] = SETTINGS
        
        if c == "r":
            # Save to Excel
            if not os.path.exists(results_file):
                df = pd.DataFrame(columns=["id", "relevant", "reason", "summary", "settings", "timestamp"])
            else:
                df = pd.read_excel(results_file)

            df = pd.concat([df, pd.DataFrame([result])], ignore_index=True)
            df.to_excel(results_file, index=False)
            print(f"Result added to {results_file}")

        elif c == "e":
            # Save to Excel
            if not os.path.exists(results_file):
                df = pd.DataFrame(columns=["id", "publication_date", "author_name", "author_university", "author_university_country", "settings", "timestamp"])
            else:
                df = pd.read_excel(results_file)
            
            for author in result.get("authors", []):
                author_result = {
                    "id": result["id"],
                    "publication_date": result.get("publication_date"),
                    "author_name": author.get("name"),
                    "author_university": author.get("university_name"),
                    "author_university_country": author.get("university_country"),
                    "settings": SETTINGS,
                    "timestamp": result["timestamp"]
                }
            
                df = pd.concat([df, pd.DataFrame([author_result])], ignore_index=True)

            df.to_excel(results_file, index=False)

            print(f"Result added to {results_file}")
        
        print("Response:", result)
        
        time.sleep(2)  # delay to avoid rate limits
