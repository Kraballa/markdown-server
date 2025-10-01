from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline

from typing import Sequence

from markdown_it.renderer import RendererProtocol
from markdown_it.utils import EnvType, OptionsDict
from markdown_it.token import Token

from .findend import find_end

def superscript_plugin(md: MarkdownIt) -> None:
    """
    implements LaTeX syntax for superscript. example usage:

    `regular text, ^{text in superscript}`
    """
    md.inline.ruler.after("strikethrough", "superscript_inline", superscript_inline)
    md.add_render_rule("superscript_inline", render_superscript_inline)

def superscript_inline(state: StateInline, silent: bool) -> bool:
    start = state.pos
    max = state.posMax
    
    if start + 2 > max:
        return False

    if state.src[start] != "^":
        return False
    if state.src[start+1] != "{":
        return False
    pos = start + 2

    end = find_end(state, pos, '}')
    if end < 0:
        return False

    pos = end
    
    if not silent:
        tokens: list[Token] = []
        state.md.inline.parse(state.src[start+2:pos], state.md, state.env, tokens)

        token = state.push("superscript_inline", "", 0)
        token.content = state.src[start+2:pos]

    state.pos = pos+1
    return True


def render_superscript_inline(self: RendererProtocol, 
                              tokens: Sequence[Token],
                              idx: int,
                              options: OptionsDict,
                              env: EnvType) -> str:

    content = tokens[idx].content
    return f"<sup>{content}</sup>"