from mcp.server.fastmcp import FastMCP

# 定义一个天气查询的mcp server
mcp_server = FastMCP(
    "weather_server",
    host="127.0.0.1",
    port=8001
)

@mcp_server.tool()  # 向mcp_server中注册一个add函数
def search_hotel(city, check_in: str = "2026-10-14", check_out: str = "2026-10-15") -> str:
    """搜索指定城市的酒店"""
    hotels = {
        "杭州": [
            {"name": "杭州香格里拉酒店", "price": 800, "address": "西湖大道", "rating": 5.0},
            {"name": "杭州如家连锁酒店", "price": 250, "address": "望江路", "rating": 4.9},
        ],
        "广州": [
            {"name": "广州白天鹅酒店", "price": 900, "address": "广州市荔湾区沙面南街", "rating": 4.9},
            {"name": "广州777快捷酒店", "price": 200, "address": "广州市天河区体育西路", "rating": 4.2},
        ]
    }
    if city in hotels:
        result = f"{city}酒店推荐 入住：{check_in} 离店：{check_out} \n"
        for hotel in hotels[city]:
            result += f"名称：{hotel['name']}，价格：{hotel['price']}，地址：{hotel['address']}，评分：{hotel['rating']}\n"
        return result
    else:
        return "该城市暂无酒店信息"

    
if __name__ == "__main__":
    mcp_server.run(transport="streamable-http")
