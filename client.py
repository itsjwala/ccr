import logging as log
from utility import *


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
            result.append("Time :\n{}\n".format(self.time))
            result.append("Memory :\n{}\n".format(self.memory))
            result.append("Output :\n{}".format(self.output))
        elif(self.errors):
            if type(self.errors) is list:
                result.append("Error/s :\n{}".format("\n".join(self.errors)))
            elif type(self.errors) is str:
                result.append("Error/s :\n{}".format(self.errors))
            else:
                result.append("Error/s : type is {}".format(type(self.errors)))
        return ''.join(result)


class Client:
    def __init__(self, url):
        self.url = url
        self.request_headers = {}
        self.request_headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        self.request_headers['accept-encoding'] = 'gzip, deflate, br'
        self.request_headers['x-requested-with'] = 'XMLHttpRequest'
        self.request_headers['Content-Type'] = 'application/x-www-form-urlencoded ; charset=UTF-8'
        self.request_body = {}

    def hit(self):
        return requests.post(self.url, data=self.request_body, headers=self.request_headers)

    def run(self, source_code, input, language, extension):
        log.warning("client {} running".format(self))
        id = None
        found_id = False
        if(language):
            try:
                id = supported_languages[language]
                found_id = True
            except KeyError:
                raise Exception("{} is not a supported language\nccr --help".format(language))

        if(not found_id):
            try:
                id = get_id_from_file_extension(extension)
            except KeyError:
                raise Exception("{} is not a supported extension\nccr --help".format(extension))
        try:
            return self._run(source_code=source_code, input=input, lang_code=self.get_lang(id))
        except KeyError:
            log.warning("{} is not supported client for language:{} and/or file extension:{}".format(self, language, extension))
        except Exception as e:
            log.error("something went wrong {}".format(e))


class GeeksForGeeksClient(Client):
    def __init__(self):
        super().__init__('https://ide.geeksforgeeks.org/main.php')

    def get_lang(self, id):
        try:
            return geeksforgeeks_languages_map[id]
        except KeyError as e:
            raise e

    def _run(self, lang_code, source_code, input=None):
        self.request_body['lang'] = lang_code
        self.request_body['code'] = source_code
        if(input):
            self.request_body['input'] = input
        response = self.hit()
        response_native = response.json()
        rntError = response_native['rntError']
        cmpError = response_native['cmpError']
        errors = []
        if(cmpError):
            errors.append(cmpError)
        if(rntError):
            errors.append(rntError)

        return ExecutionResult(response_native['output'], errors, response_native['time'], response_native['memory'])

    def __str__(self):
        return "GeeksForGeeks"


class CodechefClient(Client):
    def __init__(self):
        super().__init__('https://www.codechef.com/api/ide/run/all')
        # self.request_headers['referer'] = 'https://www.codechef.com/ide'

    def get_lang(self, id):
        try:
            return codechefs_languages_map[id]
        except KeyError as e:
            raise e

    def _run(self, lang_code, source_code, input=None):
        self.request_body['language'] = lang_code
        self.request_body['sourceCode'] = source_code
        if(input):
            self.request_body['input'] = input
        response = self.hit()
        response_native = response.json()
        timestamp = response_native['timestamp']
        # self.request_headers['ide'] = response.cookies['ide']
        # self.request_headers['AWSALB'] = response.cookies['AWSALB']
        output = time = memory = None
        errors = []
        while True:
            try:
                response = requests.get("{}?timestamp={}".format(self.url, timestamp), headers=self.request_headers)
                response_native = response.json()
                output = response_native['output']
                stderr = response_native['stderr']
                if(stderr):
                    errors.append(stderr)
                cmpinfo = response_native['cmpinfo']
                if(cmpinfo):
                    errors.append(cmpinfo)

                time = response_native['time']
                memory = response_native['memory']
                return ExecutionResult(output, errors, time, memory)
            except Exception:
                pass

    def __str__(self):
        return "CodeChef"


# class LeetCodeClient(Client):
#     def __init__(self):
#         super().__init__('https://leetcode.com/playground/api/runcode')
#         # self.request_headers['Content-Type'] = 'application/json ; charset=UTF-8'
#         # self.request_headers['referer'] = 'https://leetcode.com/playground/new'

#     def get_lang(self, id):
#         try:
#             return leetcodes_languages_map[id]
#         except KeyError as e:
#             raise e

#     def _run(self, lang_code, source_code, input=None):
#         # self.request_body = '{"data_input":"{}","lang":"{}","typed_code":"{}"}'.format(input, lang_code, source_code)
#         self.request_body['lang'] = lang_code
#         self.request_body['typed_code'] = source_code
#         if(input):
#             self.request_body['data_input'] = input

#         response = self.hit()
#         print(response.headers)
#         print(response.text)

#         # response_native = response.json()

#     def __str__(self):
#         return "LeetCode"
