import json
import logging
import shlex
from file_interface import FileInterface

class FileProtocol:
    def __init__(self):
        self.file = FileInterface()

    def proses_string(self, string_datamasuk=''):
        string_process = string_datamasuk.split();
        truncated_string_process = " ".join(string_process[:2])
        logging.warning(f"string diproses: {truncated_string_process}")
        c = shlex.split(string_datamasuk)
        try:
            c_request = c[0].strip().upper()
            logging.warning(f"memproses request: {c_request}")
            params = c[1:]
            cl = getattr(self.file, c_request.lower())(params)
            return json.dumps(cl)
        except Exception as e:
            logging.warning(f"error: {str(e)}")
            return json.dumps(dict(status='ERROR', data='request tidak dikenali'))

if __name__ == '__main__':
    fp = FileProtocol()