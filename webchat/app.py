from flask import Flask, render_template, request, jsonify
import sys
import os
import json
import threading
import time

# 添加父目录到路径，以便导入ds模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ds import AI

app = Flask(__name__)

# 配置文件路径
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "api.json")

# AI实例和锁
ai = None
ai_lock = threading.Lock()

# 初始化AI实例
def init_ai():
    global ai
    with ai_lock:
        ai = AI(CONFIG_FILE)
    return ai

# 初始化AI
ai = init_ai()

# 存储会话历史
sessions = {}

@app.route('/')
def index():
    """渲染主页"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """处理聊天请求"""
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    system_message = data.get('system_message', "你是一个友好的中文助手，请用简洁的语言回答问题。")
    temperature = data.get('temperature', 0.7)
    
    # 获取或创建会话历史
    if session_id not in sessions:
        sessions[session_id] = [
            {"role": "system", "content": system_message}
        ]
    else:
        # 更新系统消息
        if sessions[session_id][0]["role"] == "system":
            sessions[session_id][0]["content"] = system_message
        else:
            sessions[session_id].insert(0, {"role": "system", "content": system_message})
    
    # 添加用户消息到历史
    sessions[session_id].append({"role": "user", "content": user_message})
    
    try:
        # 调用AI获取回复
        with ai_lock:
            response = ai.chat_completion(sessions[session_id], temperature=temperature)
        assistant_reply = response.choices[0].message.content
        
        # 添加助手回复到历史
        sessions[session_id].append({"role": "assistant", "content": assistant_reply})
        
        return jsonify({
            "status": "success",
            "reply": assistant_reply
        })
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/config', methods=['GET', 'POST'])
def config():
    """获取或更新配置"""
    global ai
    
    if request.method == 'GET':
        try:
            # 读取配置文件
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                # 不再自动覆盖配置文件中的模型名称
                # 只返回当前加载的模型信息，但不修改配置
                with ai_lock:
                    current_model = ai.get_model()
                
                return jsonify({
                    "status": "success",
                    "config": config_data,
                    "current_model": current_model  # 单独返回当前模型
                })
            else:
                return jsonify({
                    "status": "error",
                    "message": "配置文件不存在"
                }), 404
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    elif request.method == 'POST':
        try:
            data = request.json
            config_data = data.get('config', {})
            
            # 验证配置
            if not config_data.get('BaseUrl') or not config_data.get('ApiKey') or not config_data.get('Model'):
                return jsonify({
                    "status": "error",
                    "message": "配置缺少必要字段"
                }), 400
            
            # 保存配置
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4)
            
            # 重新初始化AI
            ai = init_ai()
            
            # 清空所有会话
            sessions.clear()
            
            # 获取更新后的模型名称，但不覆盖用户设置的值
            with ai_lock:
                current_model = ai.get_model()
            
            return jsonify({
                "status": "success",
                "message": "配置已保存并重新加载",
                "current_model": current_model,  # 返回当前加载的模型
                "saved_model": config_data.get('Model')  # 返回保存的模型名称
            })
        
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

if __name__ == '__main__':
    app.run(debug=True) 