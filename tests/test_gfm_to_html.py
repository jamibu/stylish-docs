from src import gfm_to_html


def test_hyperlink_from_heading():
    heading = "Testing the Heading Hyperlinker"
    expected = "testing-the-heading-hyperlinker"
    assert gfm_to_html.hyperlink_from_heading(heading) == expected

    heading = "Ignore {[(brackets)]}"
    expected = "ignore-brackets"
    assert gfm_to_html.hyperlink_from_heading(heading) == expected

    heading = "Remove, and."
    expected = "remove-and"
    assert gfm_to_html.hyperlink_from_heading(heading) == expected

    # TODO Need to look into a few more edge cases to see what VSCode does
    # - "remove . and ," == "remove--and-" (or "remove-and")


def test_link_toc():
    html_str = (
        "<html><body>"
        "<h1>This is a heading</h1>"
        "<p>This is not a heading</p>"
        "<h2>This is a (smaller) heading</h2>"
        "<h3>Don't add this one <!-- omit in toc --></h3>"
        "</body></html>"
    )
    expected = (
        "<html><body>"
        '<h1 id="this-is-a-heading">This is a heading</h1>'
        "<p>This is not a heading</p>"
        '<h2 id="this-is-a-smaller-heading">This is a (smaller) heading</h2>'
        "<h3>Don't add this one <!-- omit in toc --></h3>"
        "</body></html>"
    )
    assert gfm_to_html.link_toc(html_str) == expected
