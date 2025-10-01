from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline

from typing import Sequence

from markdown_it.renderer import RendererProtocol
from markdown_it.utils import EnvType, OptionsDict
from markdown_it.token import Token

def ruby_annotation_plugin(md: MarkdownIt) -> None:
    """
    add syntax for ruby annotations. example:

    `{a word|annotation}`
    """
    md.inline.ruler.after("image", "ruby_annotation_inline", ruby_annotation_inline)
    md.add_render_rule("ruby_annotation_inline", render_ruby_annotation_inline)

def ruby_annotation_inline(state: StateInline, silent: bool) -> bool:
    start = state.pos
    max = state.posMax

    if start + 1 > max:
        return False

    if state.src[start] != "{":
        return False
    pos = start + 1

    num_pipes = 0
    while pos < max:
        if state.src[pos] == "}":
            break
        if state.src[pos] == "|":
            num_pipes += 1
        pos += 1

    # no empty or only whitespaced subscript
    if pos == start + 1:
        return False
    if num_pipes != 1:
        return False
    
    if not silent:
        tokens: list[Token] = []
        state.md.inline.parse(state.src[start+1:pos], state.md, state.env, tokens)

        token = state.push("ruby_annotation_inline", "", 0)
        token.content = state.src[start+1:pos]

    state.pos = pos+1
    return True


def render_ruby_annotation_inline(self: RendererProtocol, 
                              tokens: Sequence[Token],
                              idx: int,
                              options: OptionsDict,
                              env: EnvType) -> str:

    parts = tokens[idx].content.split('|')

    # rp parts for browsers that don't support ruby annotations
    return f"<ruby>{parts[0]}<rp>(</rp><rt>{parts[1]}</rt><rp>)</rp></ruby>"