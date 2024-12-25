from collections import defaultdict
from typing import Dict, List, Sequence
from .tags import TAG_LUT


def tag_title(title: str) -> List[str]:
    if isinstance(title, dict):
        title = title["#text"]
    tags = set()
    title = title.lower()
    for cat, keywords in TAG_LUT.items():
        for word in keywords:
            if word in title or word.replace(" ", "-") in title:
                tags.add(cat)
                break
    return tags


def count_tags(tag_list: Sequence[Sequence[str]]) -> Dict[str, int]:
    tag_count = defaultdict(int)
    for group in tag_list:
        for tag in group:
            tag_count[tag] += 1
    return tag_count