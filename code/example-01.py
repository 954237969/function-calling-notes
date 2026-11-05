tools = [
    {
        "type": "function",
        "function": {
            "name": "add",                          # 叫什么
            "description": "将数字a与数字b相加",      # 干什么（模型靠这句判断该不该调用）
            "parameters": {                          # 要传什么参数
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "第一个数字"
                          },
                    "b": {"type": "integer", "description": "第二个数字"
                          }
                }
            },
            "required": ["a", "b"]                    # 哪些必填
        }
    }
}]
