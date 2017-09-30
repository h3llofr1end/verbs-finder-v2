from nltk import pos_tag
import collections
import functions as func
import words_functions as wf

def is_verb(word):
    if word:
        pos_info = pos_tag([word])
        return pos_info[0][1] == 'VB' or pos_info[0][1] == 'VBP'


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def get_top_verbs_in_path(path, top_size=10):
    trees = [t for t in func.get_trees(path) if t]
    words = wf.get_all_words_in_path(path)
    functions = func.get_all_function_names(trees)
    verbs = func.flat([get_verbs_from_function_name(name) for
                  name in functions])
    verbs += func.flat([get_verbs_from_function_name(name) for
                   name in words])
    return collections.Counter(verbs).most_common(top_size)