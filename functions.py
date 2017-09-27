import ast
import os
import collections
import subprocess


from nltk import pos_tag


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def is_verb(word):
    if word:
        pos_info = pos_tag([word])
        return pos_info[0][1] == 'VB' or pos_info[0][1] == 'VBP'


def is_noun(word):
    if word:
        pos_info = pos_tag([word])
        return pos_info[0][1] == 'NN'


def get_trees(_path):
    filenames = []
    trees = []
    for dirname, dirs, files in os.walk(_path, topdown=True):
        fill_filenames_array(files, filenames, dirname)
    for filename in filenames:
        trees.append(generate_tree(filename))
    return trees


def fill_filenames_array(files, filenames, dirname, max_files=100):
    gen = (file for file in files if file.endswith('.py'))
    for file in gen:
        filenames.append(os.path.join(dirname, file))
        if len(filenames) == max_files:
            break


def generate_tree(filename):
    tree = None
    with open(filename, 'r', encoding='utf-8') as attempt_handler:
        main_file_content = attempt_handler.read()
    try:
        tree = ast.parse(main_file_content)
    except SyntaxError as e:
        print(e)
    return tree


def get_all_names(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def get_nouns_from_name(name):
    return [word for word in name.split('_') if is_noun(word)]


def get_all_words_in_path(path):
    trees = [t for t in get_trees(path) if t]
    function_names = [f for f in flat(
        [get_all_names(t) for t in trees]
    ) if not (f.startswith('__') and f.endswith('__'))]
    return flat([split_snake_case_name_to_words(function_name)
                 for function_name in function_names])


def split_snake_case_name_to_words(name):
    return [n for n in name.split('_') if n]


def get_top_verbs_in_path(path, top_size=10):
    trees = [t for t in get_trees(path) if t]
    words = get_all_words_in_path(path)
    functions = get_all_function_names(trees)
    verbs = flat([get_verbs_from_function_name(name) for
                  name in functions])
    verbs += flat([get_verbs_from_function_name(name) for
                   name in words])
    return collections.Counter(verbs).most_common(top_size)


def get_top_nouns_in_path(path, top_size=10):
    trees = [t for t in get_trees(path) if t]
    words = get_all_words_in_path(path)
    functions = get_all_function_names(trees)
    nouns = flat([get_nouns_from_name(name) for
                  name in functions])
    nouns += flat([get_nouns_from_name(name) for
                  name in words])
    return collections.Counter(nouns).most_common(top_size)


def get_all_function_names(trees):
    return [f for f in flat(
        [[node.name.lower() for node in ast.walk(t) if
          isinstance(node, ast.FunctionDef)] for t in trees]) if
                 not (f.startswith('__') and f.endswith('__'))]


def get_top_functions_names_in_path(path, top_size=10):
    t = get_trees(path)
    nms = [f for f in flat([
        [node.name.lower() for node in ast.walk(t)
         if isinstance(node, ast.FunctionDef)]
        for t in t]) if not (f.startswith('__') and f.endswith('__'))]
    return collections.Counter(nms).most_common(top_size)


def get_functions_words(path, top_size=10):
    trees = get_trees(path)
    names = get_all_function_names(trees)
    split_names = flat([
        split_snake_case_name_to_words(name) for name in names
    ])
    return collections.Counter(split_names).most_common(top_size)


def get_vars_words(path, top_size=10):
    words = get_all_words_in_path(path)
    return collections.Counter(words).most_common(top_size)


def generate_report(data, type, top_size=200):
    if not type:
        return
    elif type == 'csv':
        report_file = open('report.csv', 'w+')
        for word, occurence in collections.Counter(data).most_common(top_size):
            report_file.write(word[0] + "," + str(word[1]) + "\n")
        report_file.close()
        print("Отчет был сохранен в файле report.csv")
    elif type == 'json':
        report_file = open('report.json', 'w+')
        report_file.write("{")
        for word, occurence in collections.Counter(data).most_common(top_size):
            report_file.write('"' + word[0] + '": "' + str(word[1]) + '", ')
        report_file.write("}")
        report_file.close()
        print("Отчет был сохранен в файле report.json")
    elif type == 'console':
        for word, occurence in collections.Counter(data).most_common(top_size):
            print(word)


def generate_data(folders, function):
    data = []
    for project in folders:
        path = os.path.join('.', project)
        data += function(path)
    return data


def git(*args):
    return subprocess.check_call(['git'] + list(args))


def clone_repository(link, service='git'):
    if link and service == 'git':
        git("clone", link)
    else:
        pass
