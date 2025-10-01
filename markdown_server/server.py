from flask import Flask, request, render_template, make_response, send_file
from markupsafe import Markup
from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.front_matter import front_matter_plugin # parses header info
from mdit_py_plugins.deflist import deflist_plugin
import os

from .superscript import superscript_plugin
from .subscript import subscript_plugin
from .rubyannot import ruby_annotation_plugin
from .texmathml import texmathml_plugin

md = (
    MarkdownIt('commonmark', {'breaks':True, 'html':True})
    .enable('table')
    .enable('strikethrough')
    .use(footnote_plugin)
    .use(front_matter_plugin)
    .use(deflist_plugin)

    .use(subscript_plugin)
    .use(superscript_plugin)
    .use(ruby_annotation_plugin)
    .use(texmathml_plugin)
)

tasklists_plugin(md, enabled=True) # need to enable checkboxes so we can style them on chrome

app = Flask(__name__)

not_found = Markup(md.render("<h3>file not found</h3><p>the file couldn't be found</p>"))
index = Markup(md.render("<h3>Index</h3><p>This is a basic index file, to be replaced...</p>"))

@app.get("/")
def root():
    paths = getAllMarkdownFiles()
    htmlChunks = ["<ul>"]
    for path in paths:
        htmlChunks.append(f"<li><a href={path}>{path}</a></li>")
    htmlChunks.append("</ul>")
    content = Markup(''.join(htmlChunks))
    return render_template("base.html", content=content, title="Index")

@app.get("/<path:subpath>")
def read(subpath=""):
    subpath = "./" + subpath
    if subpath.endswith(".md"):
        text = readFile(subpath)
    else:
        if os.path.exists(subpath):
            return send_file(subpath)
        else:
            return make_response("file not found", 404)

    return render_template("base.html", content=text, title="MarkdownViewer")

def readFile(path):
    if not os.path.exists(path):
        return not_found
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()
    return Markup(md.render(text))

def getAllMarkdownFiles(path="."):
    markdown_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
        for dir in dirs:
            print(dir)
    return markdown_files

def main():
    print("markdown server is running...")
    app.run()

if __name__ == "__main__":
    main()