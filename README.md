# 区块链投票系统

一个非常简单的基于区块链的投票系统，用 Python + Flask 实现。

## 功能

- 区块链核心：区块、SHA-256 哈希、工作量证明（PoW）、链验证
- 投票：每个选民只能投一票，投票被打包进新区块
- Web 界面：投票、查看实时结果、查看整条区块链

## 运行

```bash
pip install -r requirements.txt
python app.py
```

然后打开浏览器访问 http://127.0.0.1:5000

## 项目结构

```
blockchain-voting/
├── blockchain.py       # 区块链核心（区块、哈希、工作量证明）
├── app.py              # Flask Web 应用
├── templates/
│   └── index.html      # 前端页面
└── requirements.txt    # 依赖
```

## API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/candidates` | 获取候选人列表 |
| POST | `/vote` | 提交投票 `{"voter": "张三", "candidate": "Alice"}` |
| GET | `/results` | 获取投票统计结果 |
| GET | `/chain` | 查看整条区块链 |

## 说明

- 数据保存在内存中，重启后清空（仅供学习演示）。
- 每个新区块包含一次投票，通过工作量证明（难度 4，即哈希以 4 个 0 开头）保证不可篡改。
