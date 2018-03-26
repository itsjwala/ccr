import requests
import json


class ExecutionResult:
    def __init__(self, output, errors, time, memory):
        self.output = output
        self.errors = errors
        if (not errors):
            self.success = True
        else:
            self.success = False

        self.time = time
        self.memory = memory

    def __str__(self):
        result = []

        if(self.success):
            result.append("Time : {}\n".format(self.time))
            result.append("Memory : {}\n".format(self.memory))
            result.append("Output :\n{}".format(self.output))
        elif(self.errors):
            if type(self.errors) is list:
                result.append("Error/s : {}".format("".join(self.errors)))
            elif type(self.errors) is str:
                result.append("Error/s : {}".format(self.errors))
            else:
                result.append("Error/s : type is {}".format(type(self.errors)))
        return ''.join(result)


class Client:
    def __init__(self, url):
        self.url = url
        self.request_headers = {}
        self.request_headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        self.request_headers['Content-Type'] = 'application/x-www-form-urlencoded ; charset=UTF-8'
        self.request_headers['accept-encoding'] = 'gzip, deflate, br'
        self.request_headers['x-requested-with'] = 'XMLHttpRequest'
        self.request_body = {}

    def hit(self):
        return requests.post(self.url, data=self.request_body, headers=self.request_headers)


class GeeksForGeeksClient(Client):
    def __init__(self):
        self.url = 'https://ide.geeksforgeeks.org/main.php'
        super().__init__(self.url)

    def __run__(self, lang, source_code, input=None):
        self.request_body['lang'] = lang
        self.request_body['code'] = source_code
        self.request_body['input'] = input
        response = self.hit()
        response_native = json.loads(response.text)
        rntError = response_native['rntError']
        cmpError = response_native['cmpError']
        errors = []
        if(rntError):
            errors.append("Runtime Error : {}".format(rntError))
        if(cmpError):
            errors.append("Compile Error : {}".format(cmpError))

        return ExecutionResult(response_native['output'], errors, response_native['time'], response_native['memory'])


class CodechefClient(Client):
    def __init__(self):

        self.url = 'https://www.codechef.com/api/ide/run/all'
        super().__init__(self.url)
        self.request_headers['referer'] = 'https://www.codechef.com/ide'

    def __run__(self, lang_code, source_code, input=None):

        self.request_body['language'] = lang_code
        self.request_body['sourceCode'] = source_code
        self.request_body['input'] = input
        response = self.hit()
        response_native = json.loads(response.text)
        timestamp = response_native['timestamp']
        # self.request_headers['ide']=response.cookies['ide']
        # self.request_headers['AWSALB']=response.cookies['AWSALB']
        output = errors = time = memory = None

        while True:
            try:
                response = requests.get("{}?timestamp={}".format(self.url, timestamp), headers=self.request_headers)
                response_native = json.loads(response.text)
                output = response_native['output']
                errors = response_native['stderr']
                time = response_native['time']
                memory = response_native['memory']
                return ExecutionResult(output, errors, time, memory)
            except:
                pass

# myspider=GeeksForGeeksClient()

# for i in range(100):
# myspider = CodechefClient()
# result = myspider.run('Python3', './test.py', './hello.txt')
# print(result)

# # index may change in future
# codechef_languages_index = {
#     'PAS gpc (gpc 20070904)': 2,
#     'PERL (perl 5.24.1)': 3,
#     'PYTH (cpython 2.7.13)': 4,
#     'FORT (gfortran 6.3)': 5,
#     'WSPC (wspace 0.3)': 6,
#     'ADA (gnat 6.3)': 7,
#     'CAML (ocamlopt 4.01)': 8,
#     'ICK (ick 0.3)': 9,
#     'JAVA (HotSpot 8u112)': 10,
#     'C (gcc 6.3)': 11,
#     'BF (bff 1.0.6)': 12,
#     'ASM (nasm 2.12.01)': 13,
#     'CLPS (clips 6.24)': 14,
#     'PRLG (swi 7.2.3)': 15,
#     'ICON (iconc 9.5.1)': 16,
#     'RUBY (ruby 2.3.3)': 17,
#     'SCM qobi (stalin 0.3)': 18,
#     'PIKE (pike 8.0)': 19,
#     'D (gdc 6.3)': 20,
#     'HASK (ghc 8.0.1)': 21,
#     'PAS fpc (fpc 3.0.0)': 22,
#     'ST (gst 3.2.5)': 23,
#     'NICE (nicec 0.9.13)': 25,
#     'LUA (luac 5.3.3)': 26,
#     'C# (gmcs 4.6.2)': 27,
#     'BASH (bash 4.4.5)': 28,
#     'PHP (php 7.1.0)': 29,
#     'NEM (ncc 1.2.0)': 30,
#     'LISP sbcl (sbcl 1.3.13)': 31,
#     'LISP clisp (clisp 2.49)': 32,
#     'SCM guile (guile 2.0.13)': 33,
#     'JS (rhino 1.7.7)': 35,
#     'ERL (erl 19)': 36,
#     'TCL (tcl 8.6)': 38,
#     'SCALA (scala 2.12.1)': 39,
#     'C++14 (gcc 6.3)': 44,
#     'kotlin (kotlin 1.0.6)': 47,
#     'PERL6 (perl 6)': 54,
#     'NODEJS (node 7.4.0)': 56,
#     'TEXT (pure text)': 62,
#     'swift (swift 3.0.2)': 85,
#     'rust (rust 1.14.0)': 93,
#     'SCM chicken (chicken 4.11.0)': 97,
#     'PYPY (PyPy 2.6.0)': 99,
#     'CLOJ (clojure 1.8.0)': 111,
#     'GO (go 1.7.4)': 114,
#     'PYTH 3.5 (python  3.5)': 116,
#     'COB (open-cobol 1.1.0)': 118,
#     'F# (mono 4.0.0': 124
# }
