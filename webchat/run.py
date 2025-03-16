#!/usr/bin/env python
"""
启动Web聊天界面的脚本
"""
from app import app

if __name__ == '__main__':
    print("启动AI聊天Web界面...")
    print("请访问 http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 