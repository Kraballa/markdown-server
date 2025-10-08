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
    content = buildFileTree()
    return render_template("base.html", content=content, title="index")

@app.get("/<path:subpath>")
def read(subpath=""):
    subpath = "./" + subpath
    if subpath.endswith(".md"):
        text = readFile(subpath)
    else:
        if os.path.exists(subpath):
            return send_file(subpath)
        else:
            response = render_template("base.html", content=not_found, title="markdown-server")
            return make_response(response, 404)

    return render_template("base.html", content=text, title="markdown-server")

def readFile(path):
    path = path.replace("%20", " ")
    if not os.path.exists(path):
        return not_found
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()
    return Markup(md.render(text))

def buildFileTree(path="."):
    markdown_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.md'):
                filePath = os.path.join(root, file)
                filePath = filePath.replace(" ", "%20")
                markdown_files.append(filePath)

    htmlChunks = ["<ul>"]
    for file in markdown_files:
        truncated = file[2:].replace("%20", " ")
        htmlChunks.append(f"<li><a href={file}>{truncated}</a></li>")
    htmlChunks.append("</ul>")
    return Markup(''.join(htmlChunks))
    

def main():
    print("markdown server is running...")
    app.run()

if __name__ == "__main__":
    main()