# 1、定义MCP的客户端
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

async def get_tools():
    # 主要作用：连接mcpserver的
    client = MultiServerMCPClient({
            "Math":{
                "transport":"stdio",
                "command": "python",
                "args":["D:\\VSCode WorkSpace\\langchain高级\\weather_server.py"]
            }
        }
    )
    all_tools = await client.get_tools() # 获取所有工具
    return all_tools

async def test_agent():
    all_tools = await  get_tools()
    print(all_tools)
    # 2、创建一个agent
    agent = create_agent(
        model="deepseek-flash",
        tools=all_tools
    )


    # 3、调用agent
    res = await agent.ainvoke({
        "messages":[{"role":"user", "content":"请帮我查询一下北京今天的天气"}]
    })
    print(res)
    
if __name__ == '__main__':
    import asyncio
    asyncio.run(test_agent())