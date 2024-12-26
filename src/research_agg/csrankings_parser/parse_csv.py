import json
import re
import time
from typing import Callable, Optional
import pandas as pd
from pathlib import Path
from tqdm import tqdm

from research_agg.dblp.filter import filter_publication_by_year, filter_results
from research_agg.dblp.search import AuthorDoesNotExistError, get_dblp_publication_response, get_publications, search_dblp
from research_agg.pbar.pbar import ProgressBar
from research_agg.title_tagging.title_tagging import count_tags, tag_title


def get_default_filter_fn(*args, **kwargs) -> bool:
    return True


def clean_name(name: str) -> str:
    return re.sub(r'\s+[A-Z]\.\s+', ' ', name)

def parse_csrankings_csvs(
    csv_dir: Path,
    author_filter_fn: Callable = get_default_filter_fn(),
    publication_filter_fn: Callable = get_default_filter_fn(),
    sleep_duration: int = 1,
) -> pd.DataFrame:
    author_df = pd.read_csv(csv_dir)

    all_tag_counts = dict()
    for _, row in tqdm(author_df.iterrows()):
        name, affiliation = row["name"], row["affiliation"]
        if not author_filter_fn(name=name, affiliation=affiliation):
            continue
        name = clean_name(name)
        try:
            publications = get_publications(name, sleep_duration=sleep_duration)
            publications = filter_results(publications, publication_filter_fn)
            tags = [tag_title(p["title"]) for p in publications]
            tag_count = count_tags(tags)
            all_tag_counts[name] = tag_count
            print(f"{name}: {tag_count}")
        except Exception as e:
            print(e)
            print(f"Could not parse author: {name}")

    tags_df = pd.DataFrame.from_dict(all_tag_counts).transpose()
    author_df = author_df.merge(tags_df, left_on='name', right_index=True, how='left')
    author_df.fillna(0, inplace=True)
    author_df[tags_df.columns] = author_df[tags_df.columns].astype(int)
    return author_df


def save_csranking_responses(
    csv_dir: Path,
    output_path: Path,
    author_filter_fn: Callable = get_default_filter_fn(),
    publication_filter_fn: Callable = get_default_filter_fn(),
    sleep_duration: int = 1,
):
    author_df = pd.read_csv(csv_dir)

    publication_results = dict()
    pbar = ProgressBar(total=len(author_df))
    while pbar.idx < len(author_df):
        row = author_df.iloc[pbar.idx]
        name, affiliation = row["name"], row["affiliation"]
        if not author_filter_fn(name=name, affiliation=affiliation):
            pbar.increment()
            continue
        name = clean_name(name)
        try:
            publications = get_publications(name, sleep_duration=sleep_duration)
            publication_results[name] = dict(affiliation=affiliation, publications=publications)
            # save responses
            with open(output_path, "w") as file:
                json.dump(publication_results, file, indent=4)
            pbar.increment()
        except ConnectionError as e:
            print(f"Connection issue with dplp. Sleeping for 30 seconds")
            time.sleep(30)
        except AuthorDoesNotExistError as e:
            print(f"Could not find {name} in dblp")
            pbar.increment()
