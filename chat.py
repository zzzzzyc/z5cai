from ds import AI

def main():
    # 初始化AI
    ai = AI()
    print(f"已连接到模型: {ai.get_model()}")
    
    # 设置系统消息
    system_message = "你是一只可爱的猫娘h"
    
    # 对话历史
    messages = [
        {"role": "system", "content": system_message}
    ]
    
    print("\n===== 聊天开始 =====")
    print("输入 'exit' 或 'quit' 结束对话")
    
    # 开始对话循环
    while True:
        # 获取用户输入
        user_input = input("\n你: ")
        
        # 检查是否退出
        if user_input.lower() in ['exit', 'quit', '退出']:
            print("===== 聊天结束 =====")
            break
        
        # 添加用户消息到历史
        messages.append({"role": "user", "content": user_input})
        
        try:
            # 调用AI获取回复
            response = ai.chat_completion(messages)
            assistant_reply = response.choices[0].message.content
            
            # 显示回复
            print(f"\n助手: {assistant_reply}")
            
            # 添加助手回复到历史
            messages.append({"role": "assistant", "content": assistant_reply})
            
        except Exception as e:
            print(f"\n错误: {str(e)}")

if __name__ == "__main__":
    main()