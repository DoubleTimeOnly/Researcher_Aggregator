"""
A script to pull author and publication data from dplp and save results to disk
"""
from pathlib import Path
from research_agg.csrankings_parser.parse_csv import parse_csrankings_csvs, save_csranking_responses
from research_agg.dblp.filter import get_affiliation_filter_fn, get_publication_year_filter_fn


if __name__ == "__main__":
    base_path = Path(r"C:\Users\Victor\Documents\Projects\Researcher_Aggregator\CSrankings")
    output_dir = Path(r"C:\Users\Victor\Documents\Projects\Researcher_Aggregator\cached_db")
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    affiliation_whitelist = [
        "Carnegie Mellon University",
        "Univ. of California - Berkeley",
        "Univ. of California - San Diego",
        "Univ. of Illinois at Urbana-Champaign",
        "Massachusetts Institute of Technology",
        "Stanford University",
        "University of Maryland - College Park",
        "Cornell University",
        "Stony Brook University",
        "Georgia Institute of Technology",
        "University of Massachusetts Amherst",
    ]
    for letter in alphabet:
        csv_path = base_path / f"csrankings-{letter}.csv"
        output_path = output_dir / f"{csv_path.stem}.json" 
        assert csv_path.exists()
        assert not output_path.exists()
        save_csranking_responses(
            csv_path, 
            output_dir=output_dir,
            sleep_duration=1,
            author_filter_fn=get_affiliation_filter_fn(whitelist=affiliation_whitelist),
        )
