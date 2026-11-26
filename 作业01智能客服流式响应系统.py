from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.messages import AIMessage, ToolMessage
load_dotenv()


from langchain_core.tools import tool

@tool
def check_order_status(order_id: str) -> str:
    """根据订单号查询订单状态。"""
    status = {
        "ORD-12345": "已发货",
        "ORD-23456": "配送中",
        "ORD-34567": "已签收"
    }
    return status.get(order_id, "订单号不存在")

@tool
def get_product_info(product_name: str) -> str:
    """根据商品名称查询商品价格、库存和描述。"""
    products = {
        "iPhone15": "价格: 8999元, 库存: 50件, 描述: 苹果手机",
        "笔记本电脑": "价格: 10999元, 库存: 30件, 描述: 苹果笔记本",
        "耳机": "价格: 1099元, 库存: 80件, 描述: airpods"
    }
    return products.get(product_name, "商品名称不存在")

@tool
def calculate_delivery_time(city: str) -> str:
    """根据城市查询预计送达时间。"""
    delivery_times = {
        "深圳": "预计送达时间: 1-2个工作日",
        "上海": "预计送达时间: 1-2个工作日",
        "广州": "预计送达时间: 2-3个工作日",
        "云南": "预计送达时间: 2-3个工作日"
    }
    return delivery_times.get(city, "城市不存在")

agent = create_agent(
    model = "deepseek-flash",
    tools = [check_order_status, get_product_info, calculate_delivery_time],
    system_prompt="你是一个专业的电商客服，擅长根据用户的需求提供订单查询、商品信息和配送时间等服务。"
)

from langchain_core.messages import AIMessage, ToolMessage

# 流式输出
for stream_mode, chunk in agent.stream(
    {
        "messages": [
            {
                "role": "user",
                "content": "帮我查一下订单ORD-12345的状态，顺便看看这个订单里的iPhone15什么时候能到"
            }
        ]
    },
    stream_mode=["updates", "messages"]
):

    if stream_mode == "updates":
        for node_name, value in chunk.items():
            print(f"\n节点名称: {node_name}")

            for msg in value.get("messages", []):

                if isinstance(msg, AIMessage) and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        print(f"工具名称: {tool_call['name']}")
                        print(f"工具参数: {tool_call['args']}")

                elif isinstance(msg, ToolMessage):
                    print(f"工具结果: {msg.content}")

    elif stream_mode == "messages":
        message, metadata = chunk

        # 只输出模型生成的文本
        if metadata["langgraph_node"] == "model":
            if isinstance(message.content, str) and message.content:
                print(message.content, end="", flush=True)

