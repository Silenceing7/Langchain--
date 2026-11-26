from mcp.server.fastmcp import FastMCP

# 定义一个mcp server
mcp_server = FastMCP(
    "math_server",
    host="127.0.0.1",
    port=8000
)

@mcp_server.tool() # 向mcp_server中注册一个add函数
def add(a:int, b:int)->int:
    """加法函数"""
    return a + b

@mcp_server.tool() # 向mcp_server中注册一个sub函数
def sub(a, b):
    """减法函数"""
    return a - b

@mcp_server.tool() # 向mcp_server中注册一个mul函数
def mul(a, b):
    """乘法函数"""
    return a * b

@mcp_server.tool() # 向mcp_server中注册一个div函数
def div(a, b):
    """除法函数"""
    if b == 0:
        return "除数不能为0"
    return a / b

if __name__ == "__main__":
    mcp_server.run(transport="streamable-http") # 启动mcp server ，使用streamable-http协议 
