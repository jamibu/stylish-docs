from argparse import ArgumentParser
from pathlib import Path
import logging

import gfm_to_html


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    """Run convert_markdown from command line."""
    # Command line args used to point to files and API.
    args = parse_args()

    # Paths for input files
    markdown_path = Path(args.markdown)
    template_path = Path(args.template)

    # Will name the html file the same as the markdown file (just with .html)
    fname = markdown_path.stem + ".html"
    # Make output path
    output_path = markdown_path.parent / fname

    # Covert markdown file to html
    compile_markdown_file(
        markdown_path, template_path, args.markdown_api, args.title, output_path
    )


def compile_markdown_file(
    markdown_path: Path,
    template_path: Path,
    api_url: str,
    title: str,
    output_path: Path,
):
    """Read Mardown file and compile to HTML with the style of Github docs.

    Args:
        markdown_path (Path): Path to markdown file.
        template_path (Path): Path to Jinja template for output HTML.
        api_url (str): URL of API to use for compiling Markdown.
        title (str): Title attribute to use in HTML.
        output_path (Path): Path to write output HTML doc to.
    """
    # Load markdown from file
    logging.info(f'Reading provided markdown file "{markdown_path}"...')
    markdown_str = markdown_path.open("r").read()

    # Load file that outlines how our html file will look
    logging.info(f"Loading HTML template ({template_path})...")
    template_str = template_path.open("r").read()

    # Use API to convert Markdown to HTML
    logging.info(f"Convert markdown using API ({api_url})...")
    markdown_as_html = gfm_to_html.get_compiled_markdown(markdown_str, api_url)

    # Add compiled markdown to the HTML template
    logging.info(f"Styling and formatting HTML ({api_url})...")
    html_str = gfm_to_html.style_compiled_markdown(
        markdown_as_html, template_str, title
    )

    # Make Table of Contents links work in HTML file
    html_str = gfm_to_html.link_toc(html_str)

    # Write the HTML file
    logging.info(f'Writing HTML file to "{output_path}"...')
    output_path.open("w").write(html_str)

    return html_str


def parse_args():
    """Parse command line arguments for the application."""
    parser = ArgumentParser(
        "Convert Markdown (VSCode style) to HTML in the style of GitHub READMEs."
    )

    # Only required input
    parser.add_argument(
        "markdown", type=str, help="The markdown file to convert to HTML."
    )

    # Can be used to use a different template
    parser.add_argument(
        "--template",
        "-j",
        type=str,
        default="./src/template.html",
        help="File containing the Jinja template for the output HTML file.",
    )

    # Can be used to use a different API with the same input format
    parser.add_argument(
        "--markdown_api",
        "-m",
        type=str,
        default="https://api.github.com/markdown",
        help="URL for the markdown compiler API.",
    )

    # Can be used to set the document's title attribute
    parser.add_argument(
        "--title",
        "-t",
        type=str,
        default="README",
        help="Title that appears in the tab.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
