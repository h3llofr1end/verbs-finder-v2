import ast
import collections
import functions as func

def get_all_names(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_all_words_in_path(path):
    trees = [t for t in func.get_trees(path) if t]
    function_names = [f for f in func.flat(
        [get_all_names(t) for t in trees]
    ) if not (f.startswith('__') and f.endswith('__'))]
    return func.flat([split_snake_case_name_to_words(function_name)
                 for function_name in function_names])


def split_snake_case_name_to_words(name):
    return [n for n in name.split('_') if n]


def get_functions_words(path, top_size=10):
    trees = func.get_trees(path)
    names = func.get_all_function_names(trees)
    split_names = func.flat([
        split_snake_case_name_to_words(name) for name in names
    ])
    return collections.Counter(split_names).most_common(top_size)


def get_vars_words(path, top_size=10):
    words = get_all_words_in_path(path)
    return collections.Counter(words).most_common(top_size)