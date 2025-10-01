from markdown_it import MarkdownIt

from typing import Sequence

from markdown_it.renderer import RendererProtocol
from markdown_it.utils import EnvType, OptionsDict
from markdown_it.token import Token

data = {}

def frontmatterdata_plugin(md: MarkdownIt) -> None:
    """
    parses frontmatter data by injecting a rendering rule.
    """
    md.add_render_rule("front_matter", render_front_matter)

def render_front_matter(self: RendererProtocol, 
                            tokens: Sequence[Token],
                            idx: int,
                            options: OptionsDict,
                            env: EnvType) -> str:
    data = {'title': "MarkdownViewer"}
    lines = tokens[idx].content.split('\n')
    for line in lines:
        if line.count(':') <= 1:
            continue
        split = line.split(":", 2)
        data[split[0].strip()] = split[1].strip()
    print('data is', data)
    env.update(data)
    return ""