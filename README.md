# AI-Augmented Systematic Literature Review (SLR) Framework

This repository provides a **framework for automating key steps of a Systematic Literature Review (SLR)** using Large Language Models (LLMs). It enables reproducible, scalable, and configurable screening and extraction workflows by leveraging structured system prompts and batch processing of academic papers.

The implementation is designed to be **domain-agnostic**: users define their own research focus by modifying system prompts, making the framework adaptable to any research field.

This repository accompanies the methodology proposed in the thesis (see [`Research Topics`](docs/Research_Topics_Final.pdf)), which introduces an AI-augmented SLR approach.

---

## Core Concept

The framework automates two main SLR steps:

1. **Relevance Screening**

   * Classifies whether a paper meets inclusion criteria
   * Provides reasoning and summaries
   * Fully driven by customizable system prompts

2. **Metadata Extraction**

   * Extracts structured information (e.g., authors, publication year)
   * Uses consistent prompt templates for scalable processing

Both steps are:

* **Prompt-configurable**
* **Batch-processable**
* **Reproducible** (via deterministic temperature settings)

---

## Customization Philosophy

This repository is intentionally **generic**.

To adapt it to your research:

* Define your **own research questions**
* Write **custom system prompts** inside `system_prompts/`
* Adjust inclusion/exclusion logic within prompts

No changes to the core Python code are required.

---

## File Structure & Components

* **`main.py`**: The primary executable script. It handles uploading papers to OpenAI, prompting the user for the analysis mode (Relevance or Extract), sending configured prompts to the language model, and saving the output to Excel files (`results_relevance.xlsx` or `results_extract.xlsx`).
* **`papers/`**: Directory where the source documents (PDFs) should be placed prior to running the script.
* **`system_prompts/`**: Contains Markdown files mapping to different operational modes. These files consist of instructions directing the language model on how to evaluate or what to extract from the uploaded papers.
* **`helpers/random_sample.py`**: A helper script that picks a random sample of papers from the `papers/` directory. It can be used to generate a proportional sample by matching previous results.
* **`requirements.txt`**: The pip dependency file containing the essential libraries required to run the scripts.

---

## How to Run

1. **Install Dependencies**
   Make sure you have an active Python environment, then install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

2. **Add Your API Key**
   Open `main.py` and replace the placeholder API key string near the top of the file:

   ```python
   OPENAI_API_KEY = "your-api-key-here"
   ```

3. **Provide Input Data**
   Place all the document files you wish to analyze inside the `papers/` folder.

4. **Run the Script**
   Execute the main script via terminal:

   ```bash
   python main.py
   ```

5. **Choose Execution Mode**
   When prompted `Relevance (r) or extract (e) mode? [r/e]:`, type your choice and press enter:

   * **`r` (Relevance)**: Evaluates a paper's relevance to predefined criteria.
   * **`e` (Extract)**: Extracts distinct information (like publication and author details) from the papers.

6. **View Results**
   Depending on the chosen mode, check the project root context for new populated Excel files containing your parsed results (`results_relevance.xlsx` or `results_extract.xlsx`).

---

## Prompt Engineering Guidelines

To effectively use this framework:

* Define **clear inclusion/exclusion criteria**
* Use **structured outputs** (e.g., JSON-like formats)
* Include **reasoning instructions** for transparency
* Iteratively refine prompts based on validation samples

This aligns with the methodology’s **conformance checking loop**, where outputs are compared against human judgment and prompts are refined iteratively.

---

## Reproducibility & Determinism

The framework is designed for **consistent outputs**:

* Low temperature settings ensure deterministic responses
* Identical inputs yield identical outputs
* Reduces variability compared to human reviewers

---

## Disclaimer

Parts of the code in this repository were developed with the assistance of AI-based coding tools, specifically GitHub Copilot. All generated code was reviewed, adapted, and validated to ensure correctness, consistency, and alignment with the intended functionality of the framework.

---
