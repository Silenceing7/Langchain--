from mcp.server.fastmcp import FastMCP

# 定义一个天气查询的mcp server
mcp_server = FastMCP(
    "weather_server",
    host="127.0.0.1",
    port=8000
)

@mcp_server.tool() # 向mcp_server中注册一个add函数
def get_weather(city:str)->str:
    """获取指定城市的天气信息"""
    weather_data = {
        "北京":"多云转晴，温度：20℃， 空气质量：优",
        "上海":"小雨，温度：15℃， 空气质量：良",
        "广州":"阴天，温度：25℃， 空气质量：良",
        "深圳":"多云，温度：28℃， 空气质量：良",
        "成都":"多云转阴，温度：18℃， 空气质量：良",
        "杭州":"小雨，温度：16℃， 空气质量：良"
    }
    return weather_data.get(city, "该城市暂无天气数据")

if __name__ == "__main__":
    #mcp_server.run(transport="stdio") # 启动mcp server ，使用stdio协议 
    mcp_server.run(transport="streamable-http")
