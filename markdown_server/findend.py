from markdown_it.rules_inline import StateInline

def find_end(state: StateInline, start: int, token: chr) -> int:
    pos = start
    while pos < state.posMax and state.src[pos] != token:
        pos+=1

    if pos >= state.posMax:
        return -1
    return pos