from typing import Optional
import pandas as pd
from pathlib import Path
from tqdm import tqdm

from research_agg.dblp.filter import filter_publication_by_year
from research_agg.dblp.search import get_publications, search_dblp
from research_agg.title_tagging.title_tagging import count_tags, tag_title


def parse_csrankings_csvs(
    csv_dir: Path,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    sleep_duration: int = 1,
) -> pd.DataFrame:
    author_df = pd.read_csv(csv_dir)

    all_tag_counts = dict()
    for name in tqdm(author_df["name"]):
        publications = get_publications(name, sleep_duration=sleep_duration)
        publications = filter_publication_by_year(publications, min_year=min_year, max_year=max_year)
        tags = [tag_title(p["title"]) for p in publications]
        all_tag_counts[name] = count_tags(tags)

    tags_df = pd.DataFrame.from_dict(all_tag_counts).transpose()
    author_df = author_df.merge(tags_df, left_on='name', right_index=True, how='left')
    author_df.fillna(0, inplace=True)
    author_df[tags_df.columns] = author_df[tags_df.columns].astype(int)
    return author_df
