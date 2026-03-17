import gradio as gr
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

# OpenAI 兼容 API 配置
API_BASE = 'http://127.0.0.1:5000/v1'
API_KEY = ''
SYSTEM = '''你叫Symeru，是一个AI助手。'''

# 初始化 OpenAI 客户端
client = OpenAI(api_key=API_KEY, base_url=API_BASE)

# 自定义 Gradio 样式
custom_css = """
#chat {
    height: 80vh;
}
"""

def chat(message, history):
    """处理聊天消息并返回 AI 响应"""
    # 将历史消息转换为 OpenAI 格式
    messages: list[ChatCompletionMessageParam] = [{"role": "system", "content": SYSTEM}]
    # Gradio 新版 history 格式：[{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}, ...]
    for msg in history:
        messages.append(msg)
    messages.append({"role": "user", "content": message})
    
    try:
        # 调用 OpenAI 兼容 API
        response = client.chat.completions.create(
            model="symeru",
            messages=messages,
            stream=True
        )
        
        # 流式返回响应
        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                yield full_response
    except Exception as e:
        yield f"错误：{str(e)}"

# 创建 Gradio 聊天界面
with gr.Blocks() as demo:
    gr.Markdown("# 欢迎体验 Symeru")
    
    with gr.Column(elem_id='chat'):
        chatbot = gr.ChatInterface(
            fn=chat,
            examples=["你好，请介绍一下自己", "什么是人工智能？", "如何学习编程？"]
        )

if __name__ == "__main__":
    demo.launch(css=custom_css)
