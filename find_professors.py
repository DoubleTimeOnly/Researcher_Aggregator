import json
from pathlib import Path
from tqdm import tqdm

from research_agg.dblp.filter import filter_publication_by_year
from research_agg.title_tagging.title_tagging import count_tags, tag_title


HERE = Path(__file__).parent


def professor_generator():
    cache = HERE / "cached_db"
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for letter in alphabet:
        data_path = cache / f"csrankings-{letter}.json"
        with open(data_path, "r") as file:
            data = json.load(file)
        for name, entry in data.items():
            yield name, entry

preferred_tags = {
    # "vision language": 1,
    # "multi modal": 1,
    # "nerf": 1,
    # "image synthesis": 1,
    # "generative": 1,
    # "pose estimation": 1,
    # "3d": 0.5,
    "object detection": 1,
    # "segmentation": 1,
    # "classification": 1,
    # "distillation": 1,
    "real time": 0.5,
    "nlp": -0.5,
}



if __name__ == "__main__":
    cache = HERE / "cached_db"
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    professor_tags = dict()

    for author, entry in tqdm(professor_generator()):
        # TODO filter by venue
        publications = filter_publication_by_year(results=entry["publications"], min_year=2022)
        publication_titles = set([
            p["title"] if not isinstance(p["title"], dict) else p["title"]["#text"] for p in publications
        ])    # remove duplicate titles
        tags = [tag_title(title) for title in publication_titles]
        tag_distribution = count_tags(tags)
        similarity = sum([preferred_tags.get(tag, 0)*count for tag, count in tag_distribution.items()])
        professor_tags[author] = dict(tags=dict(tag_distribution), similarity=similarity, affiliation=entry["affiliation"])
    
    for author, entry in sorted(professor_tags.items(), key=lambda x: x[1]["similarity"]):
        print(50*'-')
        print(f"{author} ({entry["affiliation"]}): {entry["tags"]}")