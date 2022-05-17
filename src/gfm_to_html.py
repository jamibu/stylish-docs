import re
import requests

from bs4 import BeautifulSoup
from jinja2 import Template


def style_compiled_markdown(
    content_str: str, template_str: str, title: str = "README"
) -> str:
    """Add compiled markdown (html) to HTML template.

    Used to add basic styling and structure to the provided HTML.

    Args:
        content_str (str): Compiled markdown (HTML) to be added to the template
        template_str (str): Template to add the compiled markdown to
        title (str, optional): What to add to title attribute in HTML.
            Defaults to "README".

    Returns:
        str: Complied markdown content within the provided HTML template.
    """
    # Create jinja template that we will use to make our docs file
    template = Template(template_str)

    # Get HTML as string basesd on template and provided markdown
    html_str = template.render(title=title, content=content_str)

    return html_str


def link_toc(html_str: str, parser: str = "lxml") -> str:
    """Add hyperlinks to VSCode markdown compiled using Github's markdown API.

    VSCode's markdown editor can automatically create and update a table of
    contents. This function makes this toc work after the Markdown is converted
    to github flavoured markdown.

    - Hyperlinks are ignored if "<!-- omit in toc -->" comment is present.
    - Does not build TOC

    Args:
        html_str (str): HTML to add link tags to
        parser (str, optional): Beautiful Soup parser to use

    Returns:
        str: HTML as string with links for TOC added to headings
    """
    # Use Beautiful Soup to help navigate the html
    soup = BeautifulSoup(html_str, parser)

    # Iterate through html to find all headings
    for h in soup.find_all(re.compile("^h[1-6]$")):
        # Comments allow headings to be admitted from table of contents
        if "<!-- omit in toc -->" in str(h):
            continue

        # Get heading as a string so we can change it to add a hyperlink
        heading_text = h.get_text().strip()

        # Write hyperlink tag around heading text
        hyperlink_text = hyperlink_from_heading(heading_text)

        # Add id to heading with the hyperlink
        h.attrs["id"] = hyperlink_text

        # Unwanted text and/or tags can be added by the markdown complier
        # This makes sure we just have the heading text
        h.string = heading_text

    return str(soup)


def hyperlink_from_heading(heading: str) -> str:
    """Wrap a hyperlink tag around text within heading tag based on it's text.

    Adding this hyperlink will allow it to be linked to from other parts of
    the page (e.g. a table of contents). The link is formatted the same as
    VSCode's automatically generated table of contents.

    Args:
        heading (str): The heading that we will be adding the hyperlink to

    Returns:
        str: Hyperlink tag containing the heading text
    """
    # Remove characters that we don't want in the hyperlink (these are not
    # included in the auto generated VSCode TOC).
    value = re.sub(r"[\[\](){}.,]", "", heading)
    # Everything is lowercase is VSCode TOC and spaces are replaced with -
    return value.lower().replace(" ", "-")


def get_compiled_markdown(markdown: str, api_url: str) -> str:
    """Calls the Github Flavoured Markdown API to convert Markdown to HTML.

    Args:
        markdown (str): Markdown to convert
        api_url (str): Url for API (Could use another API as long as the
            inputs and outputs are the same).

    Raises:
        Exception: Request did not return 200.

    Returns:
        str: HTML using Github Flavoured Markdown
    """
    # Request body only needs to contain the markdown we want to convert
    request = {
        "text": markdown,
    }

    # Posting the request body will return the compiled markdown (i.e. HTML)
    response = requests.post(api_url, json=request)

    # Catch failed requests
    if response.status_code != 200:
        raise Exception(f"Request to Github API failed: {response.text}")

    # Just want to return the compiled markdown
    return response.text
