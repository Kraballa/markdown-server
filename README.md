# Markdown Server

A simple server for rendering Markdown files.

## Installation
<!-- 
```bash
pip install markdown-server
``` -->

## Usage

```bash
cd <your dir>
markdown-server
```

## Features
- Starts a python flask server in the current directory that renders and serves markdown files
- Simple web interface for browsing all markdown files at path `/`
- Supports images and cross-file links
- Is opinionated with a base jinja template for the flask server and styling
- Support for common Markdown extensions plus the following custom ones:

| idea             | HTML result              | markdown syntax             |
| :--------------- | :----------------------- | :-------------------------- |
| superscript      | `<sup>` tag              | `^{superscripted text}`     |
| subscript        | `<sub>` tag              | `_{subscripted text}`       |
| ruby annotation  | `<ruby>` tag and friends | `{some text \| annotation}` |
| amsmath notation | `<math>` (google MathML) | `$ *amsmath notation* $`    |

## Development

### Setup

1. Clone this repository
2. Install dependencies: `pip install -e .`
3. Run the development server: `python -m markdown_server.cli`
