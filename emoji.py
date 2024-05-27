import json
# import Levenshtein
# import word2emoji
import re
pattern = re.compile(r'[^a-z\s]+')

def get_words(s):
    s = s.lower().strip()
    s = pattern.sub('', s)
    return s.split(' ')

stopwords = set(['and', 'or', 'the'])
def remove_stopwords(s):
    return s - stopwords

demoji = json.load(open('codes.json', 'r'))
# print(len(demoji))
enmoji = {v: k for k, v in demoji.items()}

wordsets = [(remove_stopwords(set(get_words(k))), v) for k, v in enmoji.items()]

def search(s):
    swords = set(get_words(s))
    # print(swords)

    candidates = {}
    for wordset, emoji in wordsets:
        sim = len(wordset.intersection(swords))
        if sim > 0:
            candidates[emoji] = sim / len(wordset)

    return candidates

def get_top_emoji(s):
    s = search(s)
    if len(s):
        return sorted(s.items(), key=lambda x: -x[1])[0][0]
    return None

if __name__ == '__main__':
    for test in [
        "Strawberries & Cream",
        "Maple Waffle",
        "Honeycomb",
        "Dark Chocolate & Sea Salt (vegan)",
        "Vanilla",
        "SECRET FLAVOUR!",
        "Salted Roasted Peanut",
        "Mitcher's Small Batch Bourbon (+2£)",
        "Coffee",
        "Alphonso Mango Sorbet (v)",
        "Coconut & Ube (v)",
        "Cherry & Damson Sorbet (v)",
        "Milk and Brownies",
    ]:
        s = search(test)
        smax = sorted(s.items(), key=lambda x: -x[1])[:3]
        print(test, smax)