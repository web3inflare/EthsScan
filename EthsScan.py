"""
@Time ： 2023/11/9 00:56
@Auth ： Web3inFlare
@File ：EthsScan.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""
import binascii
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import requests
from tqdm import tqdm

from debug import logger

with open("Scan_Config.json", "r") as f:
    file = json.loads(f.read())
    task_thread = file['task_thread']
    work_thread = file['work_thread']
    tick_list = file['tick_list']
    if file["proxy"] == "":
        proxy = None
        logger.info(f"[*] 类型: 无代理检测 任务线程:{task_thread} 工作线程:{work_thread}")
    else:
        logger.info(f"[*] 类型: 代理检测 任务线程:{task_thread} 工作线程:{work_thread}")
        proxy = file['proxy']


class EthsScan(object):

    def run(self):
        with ThreadPoolExecutor(max_workers=task_thread) as executor:

            logger.info(f"[*] 开始检测铭文!")
            for i in tick_list:
                executor.submit(self._work, i['tick'], i['start_number'], i['end_number'], i['amt'])

    def _work(self, tick_name, start_number, end_number, amt):
        work_result = []
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        with ThreadPoolExecutor(max_workers=work_thread) as executor:
            tasks = range(start_number, end_number + 1)
            futures = [executor.submit(self._verify, tick_name, amt, i) for i in tasks]
            with tqdm(desc=f"{current_time} | {tick_name}", total=len(futures), leave=False) as progress_bar:
                for future in futures:
                    work_result.append(future.result())  # 等待任务完成
                    progress_bar.update(1)
        success_count = sum(1 for result in work_result if result)
        logger.success("[*] {} 有效数量：{}/{}".format(tick_name,success_count,len(futures)))

    def _verify(self, tick_name, amt, tick_number):
        data = 'data:,{{"p":"erc-20","op":"mint","tick":"{}","id":"{}","amt":"{}"}}'.format(tick_name, tick_number, amt)
        hex_id = '0x' + binascii.hexlify((data.encode())).decode()
        hash_id = hashlib.sha256(bytes.fromhex(hex_id[2:])).hexdigest()
        url = f"https://ethscriber.xyz/api/ethscriptions/exists/{hash_id}"
        response = requests.get(url, proxies={
                "http": proxy,
                "https": proxy
            })
        if response.status_code == 200:
            result = response.json()
            if not result['result']:
                self._write_file(tick_name, data)
                return True
        else:
            logger.error(f"[*]未知错误: {response.json()} {response.status_code}")

    @staticmethod
    def _write_file(tick_name, data):
        with open(f"{tick_name}.txt", "a+") as files:
            files.write(f"{data}\n")


if __name__ == '__main__':
    Scan = EthsScan()
    Scan.run()
