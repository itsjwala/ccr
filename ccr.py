import logging as log
from client import *


class CCR:
    def __init__(self, lang, source_file_path, input_file_path):
        self.lang = lang
        try:
            self.ext = source_file_path.split(".")[-1]
        except Exception:
            log.warning("unable to get file extension from file {}".format(source_file_path))
        try:
            self.source_code = self.read_file(source_file_path)
            if(input_file_path):
                self.input = self.read_file(input_file_path)
            else:
                self.input = None
        except Exception as e:
            log.critical('Exception occured at CCR init {}'.format(e))
            raise e
        self.clients = [CodechefClient(), GeeksForGeeksClient()]

    def read_file(self, file):
        content = ''
        try:
            with open(file) as f:
                content = f.read()
        except Exception as e:
            raise e
        return content

    def execute(self):
        try:
            for client in self.clients:
                result = client.run(self.source_code, self.input, self.lang, self.ext)
                print(result)
        except Exception as e:
            log.error("something went wrong {}".format(e))
            raise e
