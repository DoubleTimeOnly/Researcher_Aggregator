from research_agg.dblp.filter import filter_publication_by_year
from research_agg.dblp.search import search_dblp
from research_agg.title_tagging.title_tagging import count_tags, tag_title


if __name__ == "__main__":
    professor = "Deva Ramanan"
    publications = search_dblp(query=professor)
    publications = filter_publication_by_year(publications, min_year=2020, max_year=None)

    publications.sort(key=lambda x: int(x["info"]["year"]), reverse=True)
    tags = [tag_title(p["info"]["title"]) for p in publications]
    tag_count = count_tags(tags)
    print(tag_count)
    
    for p in publications[:10]:
        print(f"{p["info"]["year"]}: {p["info"]["title"]}")