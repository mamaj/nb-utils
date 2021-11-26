import re


def filter_between(str, before, after):
    if not str:
        return None
    before = before or ''
    after = after or ''

    if not before and not after:
        return str

    pattern = re.escape(before) + '(.*?)' + re.escape(after)
    if ans := re.search(pattern, str, flags=re.S):
        return ans.group(1)


def filter_code(code, remove_comment=True, remove_indent=True):
    if not code:
        return None

    result = []
    for line in code.split('\n'):
        if remove_comment:
            line = line.split('#')[0]
        if remove_indent:
            line = line.strip()
        if line:
            result.append(line)
    return '\n'.join(result)
