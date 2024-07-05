import os
import socket
import json
import base64
import logging
import struct

server_address = ('localhost', 8889)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        command_bytes = command_str.encode()
        command_length = struct.pack('!I', len(command_bytes))

        sock.sendall(command_length)
        sock.sendall(command_bytes)

        data_received = b""
        while True:
            data = sock.recv(4096)
            if data:
                data_received += data
                if b"\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = json.loads(data_received.decode())
        logging.warning("data received from server:")
        return hasil
    except Exception as e:
        logging.warning(f"error during data receiving: {str(e)}")
        return False
    finally:
        sock.close()

def remote_list():
    command_str = f"LIST"
    result = send_command(command_str)
    if result and result['status'] == 'OK':
        print("Daftar file : ")
        for nmfile in result['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str = f"GET {filename}"
    result = send_command(command_str)
    if result and result['status'] == 'OK':
        nameFile = result['data_namafile']
        file = base64.b64decode(result['data_file'])
        with open(nameFile, 'wb') as fp:
            fp.write(file)
        print(f"{nameFile} berhasil diunduh.")
        return True
    else:
        print("Gagal")
        return False

def remote_upload(filename=""):
    try:
        if filename == '':
            return None
        with open(filename, "rb") as fp:
            file = base64.b64encode(fp.read()).decode()

        command_str = f"UPLOAD {os.path.basename(filename)} {file}"
        hasil = send_command(command_str)
        if hasil["status"] == "OK":
            print(hasil["data"])
            return True
        else:
            print("Gagal")
            return False
    except Exception as e:
        logging.warning(f"Error during file upload: {str(e)}")
        return False
    
def remote_delete(filename=""):
    try:
        if filename == '':
            return None
        command_str = f"DELETE {filename}"
        hasil = send_command(command_str)
        if hasil["status"] == "OK":
            print(hasil["data"])
            return True
        else:
            print("Gagal")
            return False
    except Exception as e:
        logging.warning(f"Error during file upload: {str(e)}")
        return False

if __name__ == '__main__':
    server_address = ('localhost', 8889)
    # remote_upload('./files/rfc2616.pdf')
    # remote_list()
    # remote_get('rfc2616.pdf')
    # remote_delete('rfc2616.pdf')