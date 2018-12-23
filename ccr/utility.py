import requests
import pickle
from os import path
from pkg_resources import resource_filename

codechefs_languages_map = dict()

# leetcodes_supported_languages = ["cpp", "java", "python", "python3", "c", "csharp", "javascript", "ruby", "swift", "kotlin", "scala", "bash", "go"]
leetcodes_languages_map = dict()

# geeksforgeeks_supported_languages = ["Python", "Python3", "Cpp", "Cpp14", "Java", "Csharp", "C", "Php", "Scala", "Perl"]
geeksforgeeks_languages_map = dict()

supported_languages = dict()
supported_languages_extension = dict()


def set_codechefs_languages_mapping(id, lang_code):
    """
        codechef uses lang_code for languages to identify which interpreter/compiler to use
    """
    # for python language --lang not set then detection by extension(.py) for different python2,python3,pypy,pypy_3  Maps to pypy_3 (id = 48)
    codechefs_languages_map[id] = lang_code


def set_geeksforgeeks_language_mapping(id, geekslang):
    geeksforgeeks_languages_map[id] = geekslang


def set_leetcodes_language_mapping(id, leetslang):
    leetcodes_languages_map[id] = leetslang


def load_supported_languages():
    """
        codeched has extensive range of languages so using it as base for all supported languages by ccr
    """
    response = requests.get('https://www.codechef.com/api/ide/undefined/languages/all').json()
    id = 1
    for lang_code, payload in response['languages'].items():
        lang = "_".join(payload['full_name'].lower().split())
        # print(lang)
        supported_languages[lang] = id
        supported_languages_extension[payload['extension']] = id
        geekslang = leetslang = None
        # map codechef's supported languages to other OJ clients
        if lang == 'c++14':
            geekslang = 'Cpp14'
            leetslang = 'cpp'
        elif lang == 'java':
            geekslang = 'Java'
            leetslang = 'java'
        elif lang == 'python' or lang =="pypy":
            geekslang = "Python"
            leetslang = "python"
        elif lang == 'python3' or lang == 'pypy_3':
            geekslang = "Python3"
            leetslang = "python3"
        elif lang == 'c':
            geekslang = 'C'
            leetslang = 'c'
        elif lang == 'c#':
            geekslang = 'Csharp'
            leetslang = 'csharp'
        elif lang == 'scala':
            geekslang = 'Scala'
            leetslang = 'scala'
        elif lang == 'php':
            geekslang = 'Php'
        elif lang == 'perl':
            geekslang = 'Perl'
        elif lang == 'go':
            leetslang = 'go'
        elif lang == 'swift':
            leetslang = 'swift'
        elif lang == 'ruby':
            leetslang = 'ruby'
        elif lang == 'kotlin':
            leetslang = 'kotlin'
        elif lang == 'bash':
            leetslang = 'bash'

        if geekslang:
            set_geeksforgeeks_language_mapping(id, geekslang)
        if leetslang:
            set_leetcodes_language_mapping(id, leetslang)
        set_codechefs_languages_mapping(id, payload['id'])

        id += 1


def get_id_from_file_extension(ext):
    try:
        return supported_languages_extension[ext]
    except KeyError:
        return None


def dump_pickle(path,data):
    try:
        with open(path,"wb") as f:
            pickle.dump(data,f)
    except Exception as e:
        raise e
def load_pickle(path):
    try:
        with open(path,"rb") as f:
            data = pickle.load(f)
        return data
    except Exception as e:
        raise e

# delete pickle if new language added in codechef api
try:
    #during devlopment use this
    # sl_path = path.join(path.dirname(path.realpath(__file__)),"pickle/supported_languages.pickle")
    # sle_path = path.join(path.dirname(path.realpath(__file__)),"pickle/supported_languages_extension.pickle")
    # clm_path = path.join(path.dirname(path.realpath(__file__)),"pickle/codechefs_languages_map.pickle")
    # glm_path = path.join(path.dirname(path.realpath(__file__)),"pickle/geeksforgeeks_languages_map.pickle")

    #for packaging use below
    sl_path = resource_filename("ccr","pickle/supported_languages.pickle")
    sle_path = resource_filename("ccr","pickle/supported_languages_extension.pickle")
    clm_path = resource_filename("ccr","pickle/codechefs_languages_map.pickle")
    glm_path = resource_filename("ccr","pickle/geeksforgeeks_languages_map.pickle")

    supported_languages = load_pickle(sl_path)
    supported_languages_extension = load_pickle(sle_path)
    codechefs_languages_map = load_pickle(clm_path)
    geeksforgeeks_languages_map = load_pickle(glm_path)

except Exception:
    load_supported_languages()
    try:
        dump_pickle(sl_path,supported_languages)
        dump_pickle(sle_path,supported_languages_extension)
        dump_pickle(clm_path,codechefs_languages_map)
        dump_pickle(glm_path,geeksforgeeks_languages_map)
    except Exception:
        print("unable to dump pickle data..")

def supported_language_cli_output_maker():
    """
        get the output and cut paste in cli.py
    """
    count = 0
    for i in supported_languages:

        print("- "+i, end="\t")
        count+=1
        if(count == 3):
            print()
            count = 0

# print(supported_languages)
# print(supported_languages_extension)

# print(codechefs_languages_map)

# print(geeksforgeeks_languages_map)


