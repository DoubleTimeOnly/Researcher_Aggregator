from research_agg.dblp.filter import filter_publication_by_year


def test_filter_publication_by_year_with_max_year():
    starting_results = [
        dict(title="title1", year="2025"),
        dict(title="title2", year="1"),
        dict(title="title3", year="1999"),
        dict(title="title4", year="2023"),
    ]

    filtered_results = filter_publication_by_year(
        results=starting_results,
        min_year=None,
        max_year=2023,
    )
    assert filtered_results == [
        dict(title="title2", year="1"),
        dict(title="title3", year="1999"),
        dict(title="title4", year="2023"),
    ]


def test_filter_publication_by_year_with_min_year():
    starting_results = [
        dict(title="title1", year="2025"),
        dict(title="title2", year="1"),
        dict(title="title3", year="1999"),
        dict(title="title4", year="2023"),
    ]

    filtered_results = filter_publication_by_year(
        results=starting_results,
        min_year=2000,
    )
    assert filtered_results == [
        dict(title="title1", year="2025"),
        dict(title="title4", year="2023"),
    ]

def test_filter_publication_by_year_with_min_max_year():
    starting_results = [
        dict(title="title1", year="2025"),
        dict(title="title2", year="1"),
        dict(title="title3", year="1999"),
        dict(title="title4", year="2023"),
    ]

    filtered_results = filter_publication_by_year(
        results=starting_results,
        min_year=2000,
        max_year=2023,
    )
    assert filtered_results == [
        dict(title="title4", year="2023"),
    ]
