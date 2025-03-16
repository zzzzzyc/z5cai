import json
import os
from openai import OpenAI

class AI:
    def __init__(self, config_path="api.json"):
        """
        初始化AI类
        
        参数:
            config_path: API配置文件的路径，默认为'api.json'
        """
        self.config_path = config_path
        self.base_url = ""
        self.api_key = ""
        self.model = ""
        self.client = None
        self.load_config()
    
    def load_config(self):
        """从配置文件加载API配置"""
        try:
            if not os.path.exists(self.config_path):
                raise FileNotFoundError(f"配置文件 {self.config_path} 不存在")
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 读取配置字段
            self.base_url = config.get("BaseUrl", "")
            self.api_key = config.get("ApiKey", "")
            self.model = config.get("Model", "")
            
            if not self.base_url or not self.api_key or not self.model:
                raise ValueError("配置文件缺少必要的字段：BaseUrl、ApiKey或Model")
            
            # 初始化OpenAI客户端
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
                
            print(f"配置加载成功: URL={self.base_url}, Model={self.model}")
        
        except json.JSONDecodeError:
            raise ValueError(f"配置文件 {self.config_path} 不是有效的JSON格式")
        except Exception as e:
            raise Exception(f"加载配置时出错: {str(e)}")
    
    def get_base_url(self):
        """获取API基础URL"""
        return self.base_url
    
    def get_api_key(self):
        """获取API密钥"""
        return self.api_key
    
    def get_model(self):
        """获取模型名称"""
        return self.model
    
    def chat_completion(self, messages, stream=False, temperature=0.7, max_tokens=None):
        """
        调用AI的聊天完成接口
        
        参数:
            messages: 消息列表，格式为[{"role": "system", "content": "..."}, ...]
            stream: 是否使用流式响应，默认为False
            temperature: 温度参数，控制随机性，默认为0.7
            max_tokens: 最大生成的token数量，默认为None
            
        返回:
            如果stream=False，返回完整的响应对象
            如果stream=True，返回流式响应对象
        """
        # 构建请求参数
        params = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "temperature": temperature
        }
        
        # 添加可选参数
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
            
        # 发送请求
        try:
            response = self.client.chat.completions.create(**params)
            return response
                
        except Exception as e:
            raise Exception(f"API请求失败: {str(e)}")
    
    def get_completion(self, prompt, system_message="You are a helpful assistant"):
        """
        简单的聊天完成接口，直接返回文本内容
        
        参数:
            prompt: 用户输入的提示词
            system_message: 系统消息，默认为"You are a helpful assistant"
            
        返回:
            模型生成的文本内容
        """
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        response = self.chat_completion(messages, stream=False)
        
        try:
            return response.choices[0].message.content
        except (AttributeError, IndexError):
            raise Exception(f"无法从响应中提取内容")
    
    def __str__(self):
        """返回API配置的字符串表示"""
        # 为了安全起见，不显示完整的API密钥
        masked_key = f"{self.api_key[:5]}...{self.api_key[-5:]}" if len(self.api_key) > 10 else "***"
        return f"AI(base_url='{self.base_url}', api_key='{masked_key}', model='{self.model}')"

'''
def main():
    try:
        # 创建DeepseekAPI实例
        api = DeepseekAPI()
        print(api)
        
        # 显示API配置
        print(f"Base URL: {api.get_base_url()}")
        print(f"Model: {api.get_model()}")
        
        # 调用API示例
        print("\n=== API调用示例 ===")
        response = api.get_completion("你好，请介绍一下自己")
        print(f"模型回复: {response}")
        
    except Exception as e:
        print(f"错误: {str(e)}")

if __name__ == "__main__":
    main()
'''
