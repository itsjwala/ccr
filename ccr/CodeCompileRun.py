import logging
from .client import *
from  multiprocessing import Pool
log = logging.getLogger("ccr.CodeCompileRun")


class CCR:
    def __init__(self, source_file_path, input_file_path,lang=None):
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
        except Exception:
            raise IOError("Unable to read file {}".format(file))
        return content

    def execute(self):

        try:
            n = len(self.clients)

            args = (self.source_code, self.input, self.lang, self.ext)

            targets = map(lambda client : client.run,self.clients)

            with Pool(processes=2) as pool:
                rs = []
                for target in targets:
                    rs.append(pool.apply_async(target, args= args))


                clients_result_ids = set()
                done = False
                while len(clients_result_ids) < n and not done:

                    for i in range(len(rs)):
                        r = rs[i]

                        if r.ready():
                            ans = r.get()
                            if ans:
                                print(ans)
                                done = True
                                break
                            else:
                                clients_result_ids.add(i)

        except Exception as e:
            log.error("something went wrong in execute method : {}".format(e))
            raise e
