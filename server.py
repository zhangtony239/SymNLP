from flask import Flask, request, jsonify, Response
import os
import json
import time
import uuid

app = Flask(__name__)

# 模拟模型列表
MODELS = [
    {
        "id": "symeru",
        "object": "model",
        "created": 1773541560,
        "owned_by": "tony",
        "root": "DACI",
        "parent": None
    },
    {
        "id": "symeru-cloud",
        "object": "model",
        "created": 1773541560,
        "owned_by": "tony",
        "root": "DACI",
        "parent": None
    }
]

@app.route('/v1/models', methods=['GET'])
def list_models():
    """列出所有可用模型"""
    return jsonify({
        "object": "list",
        "data": MODELS
    })

@app.route('/v1/models/<model_id>', methods=['GET'])
def retrieve_model(model_id):
    """获取特定模型信息"""
    model = next((m for m in MODELS if m['id'] == model_id), None)
    if model:
        return jsonify(model)
    else:
        return jsonify({
            "error": {
                "message": f"The model '{model_id}' does not exist",
                "type": "invalid_request_error",
                "param": None,
                "code": "model_not_found"
            }
        }), 404

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    """处理聊天完成请求"""
    try:
        data = request.get_json()
        
        # 验证必需字段
        if 'messages' not in data:
            return jsonify({
                "error": {
                    "message": "Missing required argument messages",
                    "type": "invalid_request_error",
                    "param": "messages",
                    "code": "missing_messages"
                }
            }), 400
        
        # 获取参数
        messages = data.get('messages', [])
        model = data.get('model', '')
        if model == '':
            #返回错误：模型参数缺失
            return jsonify({
                "error": {
                    "message": "Missing model argument.",
                    "type": "invalid_request_error",
                    "param": "model",
                    "code": "missing_model"
                }
            })
        temperature = data.get('temperature', 1.0)
        max_tokens = data.get('max_tokens', 131072)
        stream = data.get('stream', False)
        
        # 检查模型是否支持
        if not any(m['id'] == model for m in MODELS):
            return jsonify({
                "error": {
                    "message": f"The model '{model}' does not exist",
                    "type": "invalid_request_error",
                    "param": "model",
                    "code": "model_not_found"
                }
            }), 404
        
        # 如果是流式响应
        if stream:
            def generate_stream():
                # 发送初始chunk，包含模型和ID等信息但没有内容
                first_chunk = {
                    "id": f"chatcmpl-{uuid.uuid4()}",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": model,
                    "choices": [
                        {
                            "index": 0,
                            "delta": {
                                "role": "assistant"
                            },
                            "finish_reason": None
                        }
                    ]
                }
                yield f"data: {json.dumps(first_chunk)}\n\n"
                
                # 模拟流式响应
                content = "这是一个模拟的流式响应。在实际实现中，这里会连接到真实的OpenAI API。"
                words = content.split()
                
                for i, word in enumerate(words):
                    chunk = {
                        "id": f"chatcmpl-{uuid.uuid4()}",
                        "object": "chat.completion.chunk",
                        "created": int(time.time()),
                        "model": model,
                        "choices": [
                            {
                                "index": 0,
                                "delta": {
                                    "content": word + (" " if i < len(words) - 1 else "")
                                },
                                "finish_reason": None
                            }
                        ]
                    }
                    yield f"data: {json.dumps(chunk)}\n\n"
                    
                # 结束标记
                end_chunk = {
                    "id": f"chatcmpl-{uuid.uuid4()}",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": model,
                    "choices": [
                        {
                            "index": 0,
                            "delta": {},
                            "finish_reason": "stop"
                        }
                    ]
                }
                yield f"data: {json.dumps(end_chunk)}\n\n"
                yield "data: [DONE]\n\n"
            
            return Response(generate_stream(), mimetype="text/event-stream")
        
        # 非流式响应
        else:
            # 这里在实际应用中应该调用真正的OpenAI API
            # 现在我们模拟响应
            content = "这是一个模拟的响应。在实际实现中，这里会连接到真实的OpenAI API。"
            
            response_data = {
                "id": f"chatcmpl-{uuid.uuid4()}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": model,
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": content
                        },
                        "logprobs": None,
                        "finish_reason": "stop"
                    }
                ],
                "usage": {
                    "prompt_tokens": len(str(messages)),
                    "completion_tokens": len(content),
                    "total_tokens": len(str(messages)) + len(content)
                }
            }
            
            return jsonify(response_data)
    
    except Exception as e:
        return jsonify({
            "error": {
                "message": str(e),
                "type": "invalid_request_error",
                "param": None,
                "code": "server_error"
            }
        }), 500

@app.route('/v1/completions', methods=['POST'])
def completions():
    """处理文本完成请求"""
    try:
        data = request.get_json()
        
        # 验证必需字段
        if 'prompt' not in data:
            return jsonify({
                "error": {
                    "message": "Missing required argument prompt",
                    "type": "invalid_request_error",
                    "param": "prompt",
                    "code": "missing_prompt"
                }
            }), 400
        
        # 获取参数
        prompt = data.get('prompt', '')
        model = data.get('model', 'gpt-3.5-turbo-instruct')
        temperature = data.get('temperature', 1.0)
        max_tokens = data.get('max_tokens', 131072)
        stream = data.get('stream', False)
        
        # 如果是流式响应
        if stream:
            def generate_stream():
                # 模拟流式响应
                content = "这是一个模拟的流式响应。在实际实现中，这里会连接到真实的OpenAI API。"
                words = content.split()
                
                for i, word in enumerate(words):
                    chunk = {
                        "id": f"cmpl-{uuid.uuid4()}",
                        "object": "text_completion",
                        "created": int(time.time()),
                        "model": model,
                        "choices": [
                            {
                                "index": 0,
                                "text": word + (" " if i < len(words) - 1 else ""),
                                "finish_reason": None
                            }
                        ]
                    }
                    yield f"data: {json.dumps(chunk)}\n\n"
                    
                # 结束标记
                end_chunk = {
                    "id": f"cmpl-{uuid.uuid4()}",
                    "object": "text_completion",
                    "created": int(time.time()),
                    "model": model,
                    "choices": [
                        {
                            "index": 0,
                            "text": "",
                            "finish_reason": "stop"
                        }
                    ]
                }
                yield f"data: {json.dumps(end_chunk)}\n\n"
                yield "data: [DONE]\n\n"
            
            return Response(generate_stream(), mimetype="text/event-stream")
        
        # 非流式响应
        else:
            # 模拟响应内容
            content = "这是一个模拟的文本完成响应。在实际实现中，这里会连接到真实的OpenAI API。"
            
            response_data = {
                "id": f"cmpl-{uuid.uuid4()}",
                "object": "text_completion",
                "created": int(time.time()),
                "model": model,
                "choices": [
                    {
                        "index": 0,
                        "text": content,
                        "logprobs": None,
                        "finish_reason": "stop"
                    }
                ],
                "usage": {
                    "prompt_tokens": len(prompt),
                    "completion_tokens": len(content),
                    "total_tokens": len(prompt) + len(content)
                }
            }
            
            return jsonify(response_data)
    
    except Exception as e:
        return jsonify({
            "error": {
                "message": str(e),
                "type": "invalid_request_error",
                "param": None,
                "code": "server_error"
            }
        }), 500

@app.route('/v1/embeddings', methods=['POST'])
def embeddings():
    """处理嵌入请求"""
    try:
        data = request.get_json()
        
        input_text = data.get('input', '')
        model = data.get('model', 'text-embedding-ada-002')
        
        # 将输入转换为列表格式以便处理
        if isinstance(input_text, str):
            input_list = [input_text]
        elif isinstance(input_text, list):
            input_list = input_text
        else:
            input_list = [str(input_text)]
        
        # 生成模拟嵌入向量 (1536维)
        embeddings_result = []
        for i, text in enumerate(input_list):
            embedding_vector = [0.0] * 1536  # 模拟1536维嵌入向量
            # 在实际实现中，这里应该计算真实的嵌入向量
            embeddings_result.append({
                "object": "embedding",
                "index": i,
                "embedding": embedding_vector
            })
        
        response_data = {
            "object": "list",
            "data": embeddings_result,
            "model": model,
            "usage": {
                "prompt_tokens": sum(len(text) for text in input_list),
                "total_tokens": sum(len(text) for text in input_list)
            }
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({
            "error": {
                "message": str(e),
                "type": "invalid_request_error",
                "param": None,
                "code": "server_error"
            }
        }), 500

# 健康检查端点
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)