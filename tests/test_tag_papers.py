from research_agg.title_tagging.title_tagging import tag_title


def test_tag_paper_title():
    title = "Language Models as Black-Box Optimizers for Vision-Language Models. Add object detection keyword"
    tags = tag_title(title)
    assert set(tags) == {"vision language", "object detection"}
