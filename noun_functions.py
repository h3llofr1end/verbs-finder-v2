from nltk import pos_tag
import collections
import functions as func
import words_functions as wf

def is_noun(word):
    if word:
        pos_info = pos_tag([word])
        return pos_info[0][1] == 'NN'


def get_nouns_from_name(name):
    return [word for word in name.split('_') if is_noun(word)]


def get_top_nouns_in_path(path, top_size=10):
    trees = [t for t in func.get_trees(path) if t]
    words = wf.get_all_words_in_path(path)
    functions = func.get_all_function_names(trees)
    nouns = func.flat([get_nouns_from_name(name) for
                  name in functions])
    nouns += func.flat([get_nouns_from_name(name) for
                  name in words])
    return collections.Counter(nouns).most_common(top_size)