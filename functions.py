import ast
import os
import collections
import subprocess


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def get_trees(_path):
    filenames = []
    trees = []
    for dirname, dirs, files in os.walk(_path, topdown=True):
        fill_filenames_array(files, filenames, dirname)
    for filename in filenames:
        trees.append(generate_tree(filename))
    return trees


def fill_filenames_array(files, filenames, dirname):
    gen = (file for file in files if file.endswith('.py'))
    for file in gen:
        filenames.append(os.path.join(dirname, file))


def generate_tree(filename):
    tree = None
    with open(filename, 'r', encoding='utf-8') as attempt_handler:
        main_file_content = attempt_handler.read()
    try:
        tree = ast.parse(main_file_content)
    except SyntaxError as e:
        print(e)
    return tree


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
