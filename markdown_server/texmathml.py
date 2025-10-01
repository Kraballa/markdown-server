from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline

from typing import Sequence

from markdown_it.renderer import RendererProtocol
from markdown_it.utils import EnvType, OptionsDict
from markdown_it.token import Token

import latex2mathml.converter as texmath

from .findend import find_end

def texmathml_plugin(md: MarkdownIt) -> None:
    """
    implements inline LaTeX amsmath syntax that gets converted to HTML5-native MathML thanks to `latex2mathml`. example usage:

    `example formula: $e^{\\pi i} + 1 = 0$`
    """
    md.inline.ruler.after("strikethrough", "texmathml_inline", texmathml_inline)
    md.add_render_rule("texmathml_inline", render_texmathml_inline)

def texmathml_inline(state: StateInline, silent: bool) -> bool:
    start = state.pos
    max = state.posMax

    if start + 1 > max:
        return False

    if state.src[start] != "$":
        return False
    pos = start + 1

    end = find_end(state, pos, '$')
    if end < 0:
        return False

    pos = end
    
    if not silent:
        tokens: list[Token] = []
        state.md.inline.parse(state.src[start+1:pos], state.md, state.env, tokens)

        token = state.push("texmathml_inline", "", 0)
        token.content = state.src[start+1:pos]

    state.pos = pos+1
    return True


def render_texmathml_inline(self: RendererProtocol, 
                              tokens: Sequence[Token],
                              idx: int,
                              options: OptionsDict,
                              env: EnvType) -> str:

    content = tokens[idx].content
    mathml_text = texmath.convert(content)
    return f"{mathml_text}"