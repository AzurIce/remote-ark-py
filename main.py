# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import re
import socket
import subprocess
import time

BLUESTACK_CONFIG_FILE_PATH = 'D:/BlueStacks_nxt/bluestacks.conf'


def get_adb_port():
    with open(BLUESTACK_CONFIG_FILE_PATH, "r") as f:
        content = f.read()
        res = re.findall(r'bst.instance.Pie64.status.adb_port="(.*)"', content)
        if len(res) > 0:
            return int(res[0])
        else:
            exit(1)


def get_screencap():
    screencap_proc = subprocess.run(
        ['adb', '-s', f'127.0.0.1:{adb_port}', 'shell', 'screencap', '-p'],
        capture_output=True
    )
    return screencap_proc.stdout.replace(b'\r\n', b'\n')


if __name__ == '__main__':
    adb_port = get_adb_port()
    print(f'adb_port: {adb_port}')
    connect_proc = subprocess.run(['adb', 'connect', f'127.0.0.1:{adb_port}'], capture_output=True)
    print(connect_proc.stdout)

    # with open('./screen.png', 'wb') as f:
    #     a = f.write(stdout)
    #     f.close()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 9999))
    s.listen()
    while True:
        cs, addr = s.accept()

        for i in range(60):
            screen = get_screencap()
            s.send(screen)
            time.sleep(1)


