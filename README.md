# EthsScan

## 项目简介

EthsScan 是一个用于快速查重以太坊铭文（ethscriptions）索引的工具。该工具提供了多线程处理、无代理和代理模式、快速查重以及支持区间查重的功能。

## 使用方法

1. 克隆项目仓库：
```
git clone https://github.com/web3inflare/EthsScan.git
```
2. 安装依赖：
```
pip install -r requirements.txt
```
3. 修改并配置 Scan_Config.json 文件，用于指定参数和配置信息。示例配置如下
```
{
  "task_thread": 10,  // 同时进行几个铭文
  "work_thread": 10,  // 每个铭文查询线程
  "proxy": "",  // 填写HTTP代理
  "tick_list": [
    {
      "tick": "Facet",  // 铭文名字
      "start_number": 30,  // 查询区间开始
      "end_number": 40,  // 查询区间结束
      "amt": 1000  // 根据铭文设置
    },
    {
      "tick": "Facetss",
      "start_number": 30,
      "end_number": 40,
      "amt": 1000 
    }
  ]
}
```
4. 在目录下查看铭文同名Txt文档.
## 要求 
  - Python 3.8 或以上版本
## 联系方式:
  - x(twitter): Web3inflare
  - 交流社群:
  - ![wechat_group](Wechat.jpeg)
