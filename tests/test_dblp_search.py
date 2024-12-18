from research_agg.dblp.search import ResultFormat, SearchType, construct_search_url, search_dblp


def test_dblp_publication_search():
    author = "Deva Ramanan"
    results = search_dblp(
        query=author,
        search_type=SearchType.PUBLICATION,
        max_results=10,
    )
    assert isinstance(results, list)
    assert isinstance(results[0], dict)
    assert len(results) == 10


def test_construct_search_url():
    query_terms = ["hello", "world"]
    url = construct_search_url(
        query_terms=query_terms,
        search_type=SearchType.AUTHOR,
        format=ResultFormat.JSON,
        max_results=25,
        max_completion_terms=10,
    )
    assert url == "https://dblp.org/search/author/api?q=hello+world&format=json&c=10&h=25"
