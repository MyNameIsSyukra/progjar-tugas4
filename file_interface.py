import os
import json
import base64
from glob import glob

class FileInterface:
    def __init__(self):
        os.makedirs('files', exist_ok=True)
        os.chdir('files')

    def list(self, params=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK', data=filelist)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def get(self, params=[]):
        try:
            filename = params[0]
            if not filename:
                return dict(status='ERROR', data='filename kosong')
            with open(filename, 'rb') as fp:
                isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK', data_namafile=filename, data_file=isifile)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def upload(self, params=[]):
        try:
            filename = params[0]
            filedata = base64.b64decode(params[1])
            if not filename:
                return dict(status='ERROR', data='filename kosong')
            with open(filename, 'wb') as fp:
                fp.write(filedata)
            return dict(status='OK', data=f"{filename} berhasil diupload")
        except Exception as e:
            return dict(status='ERROR', data=str(e))
        
    def delete(self, params=[]):
        try:
            filename = params[0]
            if not filename:
                return dict(status="ERROR", data='filename kosong')
            if os.path.exists(filename):
                os.remove(filename)
                return dict(status="OK", data=f"{filename} berhasil dihapus")
            else:
                return dict(status="ERROR", data=f"{filename} tidak ditemukan")
        except Exception as e:
            return dict(status="ERROR", data=str(e))

if __name__ == '__main__':
    f = FileInterface()