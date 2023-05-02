import json
import pathlib
import re
import time

from asst.asst import Asst
from asst.utils import Message, Version, InstanceOptionType
from asst.updater import Updater
from asst.emulator import Bluestacks

BLUESTACK_CONFIG_FILE_PATH = 'D:/BlueStacks_nxt/bluestacks.conf'

def get_adb_port():
    with open(BLUESTACK_CONFIG_FILE_PATH, "r") as f:
        content = f.read()
        res = re.findall(r'bst.instance.Pie64.status.adb_port="(.*)"', content)
        if len(res) > 0:
            return int(res[0])
        else:
            exit(1)



@Asst.CallBackType
def my_callback(msg, details, arg):
    m = Message(msg)
    d = json.loads(details.decode('utf-8'))

    print(m, d, arg)


if __name__ == "__main__":

    # 请设置为存放 dll 文件及资源的路径
    path = pathlib.Path(__file__).parent.parent

    # 设置更新器的路径和目标版本并更新
    # Updater(path, Version.Stab.le).update()

    # 外服需要再额外传入增量资源路径，例如
    # incremental_path=path / 'resource' / 'global' / 'YoStarEN'
    Asst.load(path=path)

    # 若需要获取详细执行信息，请传入 callback 参数
    # 例如 asst = Asst(callback=my_callback)
    asst = Asst()

    # 设置额外配置
    # 触控方案配置
    asst.set_instance_option(InstanceOptionType.touch_type, 'maatouch')
    # 暂停下干员
    # asst.set_instance_option(InstanceOptionType.deployment_with_pause, '1')

    # 启动模拟器。例如启动蓝叠模拟器的多开Pie64_1，并等待30s
    # Bluestacks.launch_emulator_win(r'C:\Program Files\BlueStacks_nxt\HD-Player.exe', 30, "Pie64_1")

    # 获取Hyper-v蓝叠的adb port
    # port = Bluestacks.get_hyperv_port(r"C:\ProgramData\BlueStacks_nxt\bluestacks.conf", "Pie64_1")

    # 请自行配置 adb 环境变量，或修改为 adb 可执行程序的路径
    adb_port = get_adb_port()
    print(f'adb_port: {adb_port}')
    if asst.connect('adb.exe', f'127.0.0.1:{adb_port}'):
        print('连接成功')
    else:
        print('连接失败')
        exit()

    # 任务及参数请参考 docs/集成文档.md

    # asst.append_task('StartUp')
    # asst.append_task('Fight', {
    #     'stage': '',
    #     'report_to_penguin': True,
    #     # 'penguin_id': '1234567'
    # })
    asst.append_task('Recruit', {
        'select': [4],
        'confirm': [3, 4],
        'times': 4
    })
    # asst.append_task('Infrast', {
    #     'facility': [
    #         "Mfg", "Trade", "Control", "Power", "Reception", "Office", "Dorm"
    #     ],
    #     'drones': "Money"
    # })
    # asst.append_task('Visit')
    # asst.append_task('Mall', {
    #     'shopping': True,
    #     'buy_first': ['招聘许可', '龙门币'],
    #     'blacklist': ['家具', '碳'],
    # })
    # asst.append_task('Award')
    # asst.append_task('Copilot', {
    #     'filename': './GA-EX8-raid.json',
    #     'formation': False
    # })
    # asst.append_task('Custom', {"task_names": ["AwardBegin"]})
    asst.start()

    while asst.running():
        time.sleep(0)
