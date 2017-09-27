import sys
import functions as f


project_folders = [
    'django',
    'flask',
    'pyramid',
    'reddit',
    'requests',
    'sqlalchemy',
]

if(sys.argv[1] == 'clone'):
    f.clone_repository(sys.argv[2])
elif(sys.argv[1] == 'vnwords'):
    if(sys.argv[2] == 'verbs'):
        f.generate_report(
            f.generate_data(project_folders, f.get_top_verbs_in_path),
            sys.argv[3])
    elif(sys.argv[2] == 'nouns'):
        f.generate_report(
            f.generate_data(project_folders, f.get_top_nouns_in_path),
            sys.argv[3])
    else:
        print('enter an arguments')
elif(sys.argv[1] == 'allwords'):
    if(sys.argv[2] == 'func'):
        f.generate_report(
            f.generate_data(project_folders, f.get_functions_words),
            sys.argv[3])
    elif(sys.argv[2] == 'vars'):
        f.generate_report(
            f.generate_data(project_folders, f.get_vars_words),
            sys.argv[3])
    else:
        print('enter an arguments')
    pass
else:
    print('please enter an arguments')
