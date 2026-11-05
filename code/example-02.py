from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage

from config import Config

conf = Config()


# todo: 第一步：定义工具函数
def add(a: int, b: int) -> int:
    """
    将数字a与数字b相加
    Args:
        a: 第一个数字
        b: 第二个数字
    """
    return a + b


def multiply(a: int, b: int) -> int:
    """
    将数字a与数字b相乘
    Args:
        a: 第一个数字
        b: 第二个数字
    """
    return a * b


# 定义 JSON 格式的工具 schema

# 关键认知：函数和 schema 是两套东西，彼此没有自动关联
# - 模型：只看到 tools 这段JSON
# - 程序：只执行 add/multiply 函数

"""
  - description：模型靠它决定要不要调用。写「将数字a与数字b相加」，模型看到「2+1等于 
    多少」才知道该选 add 而不是 multiply。                                           
  - parameters.type: "object" + properties：规定参数名和类型，模型据此生成 {"a": 2,  
    "b": 1}。                                                                        
  - required：不传会报错。                                                           
  - 没有 returns 字段：模型不知道工具返回什么类型，所以结果必须通过 ToolMessage      
    显式回传。
"""

"""
  模型返回的 "name": "add" 字符串 → 在你的字典里查出真实的函数对象。字符串 "add"         
  能对上函数 add，纯靠你手写时保持命名一致——写错一个字母，模型明明调对了，你这边就       
  KeyError。                                                                             
                                                                                         
  ▎ 这就是为什么后面会学 @tool 装饰器：它能从函数签名 + docstring 自动生成               
  ▎ schema，并自动完成这个映射，不用手写、不会对不上。
"""

tools = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "将数字a与数字b相加",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "第一个数字"
                    },
                    "b": {
                        "type": "integer",
                        "description": "第二个数字"
                    }
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "multiply",  # 叫什么
            "description": "将数字a与数字b相乘",  # 干什么（模型靠这句判断该不该调用）
            "parameters": {  # 要传什么参数
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "第一个数字"
                          },
                    "b": {"type": "integer", "description": "第二个数字"
                          }
                },
                "required": ["a", "b"]  # 哪些必填
            }
        }
    }
]

# todo: 第二步：初始化模型并绑定工具
llm = ChatOpenAI(base_url=conf.base_url,
                 api_key=conf.api_key,
                 model=conf.model_name,
                 temperature=0.1)  # 工具调用是“精确选择 + 精确参数生成”，一般用 0 更稳，减少编造参数名的情况。
# 绑定工具，允许模型自动选择工具
# bind_tools 不改变模型本身，只是让之后每次 invoke 都自动带上 tools参数 —— 这就是“绑定”。
llm_with_tools = llm.bind_tools(tools, tool_choice="auto")
"""
  - tool_choice="auto"：模型自己判断调不调。其他选项：                                   
    - "none"：禁止调用                                                                   
    - "required"：强制调用至少一个                                                       
    - {"type": "function", "function": {"name": "add"}}：强制调指定的那个
"""

# todo: 第三步：调用循环 回复
query = "2+1等于多少？"
messages: list[BaseMessage] = [HumanMessage(query)]

try:
    # todo: 第一次调用
    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)
    print(f"\n第一轮调用后结果：\n{messages}")

    """
    模型看到用户问题和工具清单，返回一个 AIMessage。此时它不回答，而是“下单”：             
                                                                                         
  AIMessage(                                                                             
      content="",                          # 注意：content 通常是空的                    
      tool_calls=[{                                                                      
          "name": "add",                                                                 
          "args": {"a": 2, "b": 1},                                                      
          "id": "call_abc123"              # 这次调用的唯一编号                          
      }]                                                                                 
  )              
  id 很重要：如果一次调了多个工具，结果回来时要靠它对应上，所以下一步必须原样带回。
    """

    # 执行工具调用
    # 判断消息中是否有tool_calls，以判断工具是否被调用
    if hasattr(ai_msg, 'tool_calls') and ai_msg.tool_calls:
        for tool_call in ai_msg.tool_calls:
            # todo: 处理工具调用
            tools_dict = {"add": add, "multiply": multiply}
            # selected_tool = tools_dict[tool_call["name"].lower()]    # 如果key不存在会报错
            selected_tool = tools_dict.get(tool_call["name"].lower())  # 如果key不存在不报错，会返回None
            if selected_tool is None:
                raise ValueError(f"未知工具: {tool_call['name']}")  # 或返回一段提示给模型
            tool_output = selected_tool(**tool_call["args"])
            messages.append(ToolMessage(content=str(tool_output),  # content 必须是字符串，所以 str(3) 不是 3，否则会报错
                                        # tool_call_id（必填）必须等于tool_call["id"]，否则服务端会拒绝
                                        tool_call_id=tool_call["id"]))
        print(f"\n第二轮  message中增加tool_output 之后：\n{messages}")

        # todo: 第二次调用，将工具结果传回模型以生成最终回答
        final_response = llm_with_tools.invoke(messages)
        print(f"\n最终模型响应：\n{final_response.content}")
        """
         现在 messages 是：                                                                 
                                                                                     
              [Human: "2+1等于多少？",                                                           
               AI: tool_calls=[add(2,1)],                                                        
               Tool: "3" (tool_call_id=call_abc123)]                                             
                                                                                             
          模型读到工具结果 3，用自然语言组织答案：“2 加 1 等于 3。” —— 得到 content          
          非空的普通回复。
        """

    else:
        print("模型未生成工具调用，直接返回文本:")
        print(ai_msg.content)
except Exception as e:
    print(f"模型调用失败: {str(e)}")

"""
完整的对话历史是四种角色：

HumanMessage   → 用户提问
AIMessage      → 模型回复（可能带 tool_calls）
ToolMessage    → 工具结果（必须对应某个 tool_call_id）
SystemMessage  → 系统提示（如果有的话）

invoke(messages) 每次都是把整个列表重新发一
"""

