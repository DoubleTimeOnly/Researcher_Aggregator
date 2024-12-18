from research_agg.dblp.filter import filter_publication_by_year
from research_agg.dblp.search import search_dblp


if __name__ == "__main__":
    professor = "Deva Ramanan"
    publications = search_dblp(query=professor)
    publications = filter_publication_by_year(publications, min_year=2020, max_year=None)

    publications.sort(key=lambda x: int(x["info"]["year"]), reverse=True)
    for p in publications:
        print(f"{p["info"]["year"]}: {p["info"]["title"]}")