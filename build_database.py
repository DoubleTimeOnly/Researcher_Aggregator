from datetime import datetime
from pathlib import Path
from research_agg.csrankings_parser.parse_csv import parse_csrankings_csvs


if __name__ == "__main__":
    # csv_path = Path(r"C:\Users\Victor\Documents\Projects\Researcher_Aggregator\CSrankings\csrankings.csv")
    base_path = Path(r"C:\Users\Victor\Documents\Projects\Researcher_Aggregator\CSrankings")
    output_dir = Path(r"C:\Users\Victor\Documents\Projects\Researcher_Aggregator\cached_db")
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for letter in alphabet:
        csv_path = base_path / f"csrankings-{letter}.csv"
        assert csv_path.exists()
        author_df = parse_csrankings_csvs(csv_path, sleep_duration=2)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")  # Format: YYYYMMDD_HHMMSS
        output_path = output_dir / f"{timestamp}_{csv_path.stem}_author_dataframe.csv"
        author_df.to_csv(output_path, index=False)
