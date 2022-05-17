# Stylish docs <!-- omit in toc -->

This command line application is made to convert Markdown files to HTML in the style of Github's READMEs. To do this, a Github Flavoured Markdown compiler is called (the same used by Github) and CSS is applied to mirror the style of Github docs. This application is capable of supporting the Table of Contents that are automatically generated by VS Code's Markdown editor. Light or dark mode will be selected based on the browser preferences.

The HTML version of this README was made using this application.

## Table of Contents <!-- omit in toc -->

- [Installation](#installation)
- [Running from the to_convert folder](#running-from-the-to_convert-folder)
- [Running manually](#running-manually)
- [A note on images](#a-note-on-images)
- [HTML templates](#html-templates)

## Running from the to_convert folder

You can automatically convert one or more Markdown files by placing then in the "to_convert" folder and running from the .bat file. The converted files will be written to the "to_convert" folder under the same name as the original file.

```
./run.bat
```

## Running manually

The scripts can also be directly called on any given markdown file as follows

```
python ./src/markdown_to_html.py README.md
```

The following options are also available when running the scipt:

- `--template`: Path to a Jinja HTML template file that will define the HTML that wraps around the converted markdown
- `--markdown_api`: URL for API method used to convert markdown to HTML
- `--title`: Title that will be displayed in the browser tab

Below is an example of the python script being run directly with all optional inputs set manually. The values used in this example are the default values. You can change any of these as you wish.

```
python ./src/markdown_to_html.py README.md ^
--template template.html ^
--markdown_api http://localhost:8888/to_styled_html ^
--title README
```

When running in this manner the output HTML file will be written in the same directory as the markdown file.

## A note on images

If you add images (or other static files) in your Markdown file using relative paths you will need to be careful to maintain the relative location of the file to the HTML file (e.g. by having the HTML file in the same folder as the Mardown file)

## HTML templates

This app lays out the HTML files based on [Jinja Templates](https://jinja.palletsprojects.com/en/3.0.x/). Note that this only defines the HTML around the converted markdown which is added as one big blob. Below we can see the default template which is a very simple example of such a template. The commandline arguments for this support providing custom templates.

```html
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{{ title }}</title>
<link
  rel="stylesheet"
  href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.1.0/github-markdown.css"
  integrity="sha512-Av8h36R+zgh5kcdZXursq5ZiKVOEQ/K/M4lZcFsbPJMKfrRaUXatxZERx2s6LzAfVUcWg90Yycl4Gsfdgfd29A=="
  crossorigin="anonymous"
  referrerpolicy="no-referrer"
/>
<style>
  .markdown-body {
    box-sizing: border-box;
    min-width: 200px;
    max-width: 980px;
    margin: 0 auto;
    padding: 45px;
  }

  @media (max-width: 767px) {
    .markdown-body {
      padding: 15px;
    }
  }
</style>

<body class="markdown-body">
  {{ markdown }}
</body>
```

All this does is add our markdown in the body of the file, set some styling to make the HTML the same as Github docs, and set the title.
