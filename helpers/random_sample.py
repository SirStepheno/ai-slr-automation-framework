import os
import pandas as pd
import random

# Path constants
PAPERS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "papers")

def get_random_sample(sample_percentage: int):
    """Get a random sample of papers from the 'papers' folder with same ratio of relevant to non-relevant papers."""
    local_files = [f for f in os.listdir(PAPERS_DIR) if os.path.isfile(os.path.join(PAPERS_DIR, f))]

    # Get relevance from results.xlsx
    if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "results.xlsx")):
        results_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results.xlsx")
        results_df = pd.read_excel(results_file)
    else:
        results_df = pd.DataFrame()

    # If relevance column does not exist, return simple random sample
    if 'relevant' in results_df.columns:
        relevance_dict = dict(zip(results_df['id'], results_df['relevant']))

        relevant_papers = [f for f in local_files if relevance_dict[int(f.split(" - ")[0])]]
        non_relevant_papers = [f for f in local_files if not relevance_dict[int(f.split(" - ")[0])]]

        # Sanity check
        if (len(relevant_papers) + len(non_relevant_papers)) != len(local_files):
            raise ValueError("Mismatch between local files and relevance data.")

        num_relevant_sample = max(1, len(relevant_papers) * sample_percentage // 100)
        num_non_relevant_sample = max(1, len(non_relevant_papers) * sample_percentage // 100)

        sampled_relevant = random.sample(relevant_papers, num_relevant_sample)
        sampled_non_relevant = random.sample(non_relevant_papers, num_non_relevant_sample)

        sampled_files = sampled_relevant + sampled_non_relevant
        random.shuffle(sampled_files)
        print(f"Random sample of papers ({sample_percentage}%), with relevant and non-relevant papers:")
    else:
        num_sample = max(1, len(local_files) * sample_percentage // 100)
        sampled_files = random.sample(local_files, num_sample)
        print(f"Random sample of papers ({sample_percentage}%), without relevance data:")

    return sampled_files

if __name__ == "__main__":
    sample_percentage = 20
    sampled_files = get_random_sample(sample_percentage)
    for f in sampled_files:
        print(f)