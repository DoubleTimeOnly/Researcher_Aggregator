from research_agg.dblp.filter import filter_publication_by_year
from research_agg.dblp.search import get_publications
from research_agg.title_tagging.title_tagging import count_tags, tag_title


if __name__ == "__main__":
    professor = "Kurt Keutzer"
    publications = get_publications(professor)
    publications = filter_publication_by_year(publications, min_year=2022, max_year=None)

    publications.sort(key=lambda x: int(x["year"]), reverse=False)
    tags = [tag_title(p["title"]) for p in publications]
    tag_count = count_tags(tags)
    print(tag_count)
    
    for p in publications[:]:
        print(f"{p["year"]}: {p["title"]}")