from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient(
    {
        "weather":{
            "transport":"streamable-http",
            "url":"http://127.0.0.1:8000/mcp"
        },
        "hotel": {
            "transport":"streamable-http",
            "url":"http://127.0.0.1:8001/mcp"
        },
        "amap-maps":{
            "transport":"streamable-http", 
            "url":"https://mcp.amap.com/mcp?key=a2b269d20ffa4351a3d397eed653e269"
        }        
})

tools = await client.get_tools()
print(tools)

agent = create_agent(
    model,
    tools=tools,
    system_prompt="你是一个专业的旅行助手，能帮助用户查询天气、酒店、地图路线等信息"
)


import markdown  # pip install markdown

# 用户的问题
res = "我想去杭州旅游，帮我查一下杭州未来3天的天气，推荐几家不错的酒店，并规划从杭州东站到西湖的路线"

# ---------- 准备两个收集器，边流式边收集 ----------
tool_logs = []     # 记录工具调用过程
answer_parts = []  # 收集模型最终回答的 token

# astream 异步流式输出，同时监听两种模式：
#   updates   -> 每个节点（模型/工具）处理后的完整状态更新
#   messages  -> 模型逐个输出的 token（打字机效果）
async for mode, chunk in agent.astream(
    {"messages": [{"role": "user", "content": res}]},
    stream_mode=["updates", "messages"]
):
    if mode == "updates":
        for node, data in chunk.items():
            messages = data.get("messages", [])
            if not messages:
                continue

            last_msg = messages[-1]

            # 情况1：模型决定调用工具 -> 打印并收集
            if getattr(last_msg, "tool_calls", None):
                for tool_call in last_msg.tool_calls:
                    line = f"调用[MCP工具]：{tool_call['name']}，参数：{tool_call['args']}"
                    print(line)
                    tool_logs.append(line)

            # 情况2：工具执行完毕 -> 打印并收集
            elif getattr(last_msg, "name", None):
                line = f"[MCP工具]执行结果：{last_msg.name}-->{last_msg.content}"
                print(line)
                tool_logs.append(line)

    elif mode == "messages":
        token, metadata = chunk

        if metadata.get("langgraph_node") == "model":
            for block in token.content:
                print(block, end="", flush=True)
                answer_parts.append(block)  # 同时收集，最后拼成完整回答

answer_md = "".join(answer_parts) 


answer_html = markdown.markdown(answer_md, extensions=["tables", "fenced_code"])

logs_html = "".join(f"<li>{log}</li>" for log in tool_logs)

html_page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>杭州旅游攻略 - AI 助手报告</title>
    <style>
        body {{ font-family: "Microsoft YaHei", sans-serif; max-width: 800px;
               margin: 40px auto; padding: 0 20px; line-height: 1.8; color: #333; }}
        h1 {{ border-bottom: 2px solid #4a90d9; padding-bottom: 10px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px 12px; }}
        th {{ background: #f0f6ff; }}
        details {{ margin: 20px 0; }}
        summary {{ cursor: pointer; font-weight: bold; color: #4a90d9; }}
    </style>
</head>
<body>
    <h1>🌸 杭州旅游攻略</h1>
    <p>生成时间：{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}</p>

    {answer_html}

    <details>
        <summary>🔧 查看工具调用过程</summary>
        <ul>{logs_html}</ul>
    </details>
</body>
</html>"""

# 保存为 HTML 文件
with open("travel_report.html", "w", encoding="utf-8") as f:
    f.write(html_page)

print(" 文件已保存：travel_report.html")
