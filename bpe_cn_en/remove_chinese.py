d = {}

def is_contain_chinese(check_str):
    if "##" != check_str[:2]:
        return False
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


with open("vocab.txt") as fin:
    for i, line in enumerate(fin):
        d[i] = line.strip()

    ids = [k for k, v in d.items() if is_contain_chinese(v)]
    print(min(ids), ids)

