# AI聊天应用

这是一个基于DeepSeek API的聊天应用，包含命令行界面和Web界面。

## 项目结构

```
项目根目录/
├── api.json           # API配置文件
├── ds.py              # AI类定义
├── chat.py            # 命令行聊天界面
└── webchat/           # Web界面相关文件
    ├── app.py         # Flask应用
    ├── run.py         # Web界面启动脚本
    └── templates/     # HTML模板
        └── index.html # 聊天界面
```

## 使用方法

### 1. 配置API

在项目根目录创建`api.json`文件，内容如下：

```json
{
    "ApiKey": "你的API密钥",
    "BaseUrl": "https://api.deepseek.com",
    "Model": "deepseek-chat"
}
```

### 2. 命令行界面

运行命令行聊天界面：

```bash
python chat.py
```

### 3. Web界面

运行Web聊天界面：

```bash
cd webchat
python run.py
```

然后在浏览器中访问 http://127.0.0.1:5000

## 功能特点

- 支持命令行和Web两种界面
- 可配置API参数（URL、密钥、模型）
- 支持调整温度参数
- 支持自定义系统消息
- Web界面支持热重载配置

## 依赖项

- Python 3.6+
- OpenAI Python SDK
- Flask (Web界面) 