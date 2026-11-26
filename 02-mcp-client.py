# 1、定义MCP的客户端
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

async def get_tools():
    # 主要作用：连接mcpserver的
    client = MultiServerMCPClient(
        {
            "Math":{
                "transport":"streamable_http",
                "url":"http://127.0.0.1:8000/mcp"
            }
        }
    )
    all_tools = await client.get_tools() # 获取所有工具
    return all_tools

async def test_agent():
    all_tools = await  get_tools()
    # 2、创建一个agent
    agent = create_agent(
        model="deepseek-flash",
        tools=all_tools
    )


    # 3、调用agent
    res = await agent.ainvoke({
        "messages":[{"role":"user", "content":"请帮我计算一下 1+1"}]
    })
    print(res)
    
if __name__ == '__main__':
    import asyncio
    asyncio.run(test_agent())