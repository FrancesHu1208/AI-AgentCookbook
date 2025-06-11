"""
AutoGen Web Agent 多模态网页浏览器示例
使用 AutoGen 框架创建一个可以控制浏览器并执行网页任务的智能代理

功能特点：
1. 多模态理解：可以理解网页的视觉内容和文本内容
2. 自动化操作：能够点击、填写表单、导航等
3. 实时反馈：在控制台显示执行过程
4. 智能决策：基于页面内容做出智能决策

使用场景：
- Google 搜索并分析结果
- 网站数据收集
- 表单自动填写
- 网页内容分析
- 自动化测试

环境变量设置：
- ENDPOINT_URL: Azure OpenAI 服务端点
- DEPLOYMENT_NAME: 模型部署名称
- AZURE_API_KEY: Azure OpenAI API 密钥

运行要求：
- 需要安装 autogen-agentchat 和 autogen-ext 包
- 需要有效的 Azure OpenAI 服务访问权限
- 系统需要支持 Chromium 浏览器
"""

# 导入必要的 AutoGen 模块
from autogen_agentchat.agents import AssistantAgent  # 基础助手代理
from autogen_agentchat.ui import Console  # 控制台输出界面
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient  # Azure OpenAI 客户端
from autogen_ext.agents.web_surfer import MultimodalWebSurfer  # 多模态网页浏览代理
from autogen_agentchat.teams import MagenticOneGroupChat  # MagenticOne 团队聊天
import asyncio  # 异步编程支持
from autogen_agentchat.conditions import MaxMessageTermination  # 最大消息终止条件
from autogen_agentchat.teams import RoundRobinGroupChat  # 轮询组聊天
import os  # 操作系统环境变量


# 配置 Azure OpenAI 连接参数
# 从环境变量获取 Azure OpenAI 服务的配置信息
endpoint = os.getenv("ENDPOINT_URL", "https://ai-<endpoint>.openai.azure.com/")  # Azure OpenAI 端点
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4.1")  # 部署模型名称
api_key = os.getenv("AZURE_API_KEY")  # API 密钥

# 检查必要的环境变量
if not api_key:
    raise ValueError("AZURE_API_KEY 环境变量必须设置")

# 创建 Azure OpenAI 模型客户端
# 用于与 Azure OpenAI 服务进行通信
model_client = AzureOpenAIChatCompletionClient(
    model=deployment,  # 指定使用的模型
    azure_deployment=deployment,  # Azure 部署名称
    api_key=api_key,  # API 认证密钥
    azure_endpoint=endpoint,  # Azure 服务端点
    api_version="2025-01-01-preview"  # API 版本
)


# 创建多模态网页浏览代理
# 这是一个可以理解视觉内容并控制浏览器的智能代理
web_surfer_agent = MultimodalWebSurfer(
        name="MultimodalWebSurfer",  # 代理名称
        model_client=model_client,  # 使用上面配置的模型客户端
        headless=False,  # 设置为 False 以在图形界面模式下打开 Chromium 浏览器
        animate_actions=True  # 启用动画效果，可以看到点击动作的过程
    )

# 定义代理团队
# 使用 MagenticOne 框架创建一个包含网页浏览代理的团队
agent_team = MagenticOneGroupChat(
    [web_surfer_agent],  # 团队成员列表，目前只有一个网页浏览代理
    max_turns=13,  # 最大对话轮数限制
    model_client=model_client  # 团队使用的模型客户端
)

async def main():
    """
    主要的异步函数，执行网页浏览任务
    """
    # 运行代理团队并实时显示消息到控制台
    # 任务：导航到 GitHub 上的 AutoGen README 页面
    stream = agent_team.run_stream(task="Navigate to the AutoGen readme on GitHub.")
    
    # 其他可能的任务示例：
    # 1. Google 搜索任务：
    # stream = agent_team.run_stream(task="Search for 'Python machine learning tutorials' on Google and summarize the top 3 results.")
    
    # 2. 网站信息收集：
    # stream = agent_team.run_stream(task="Go to https://python.org and find the latest Python version.")
    
    # 3. 表单填写：
    # stream = agent_team.run_stream(task="Navigate to a contact form and fill it with sample data.")
    
    # 将代理的执行过程实时输出到控制台
    await Console(stream)
    
    # 任务完成后关闭代理控制的浏览器
    # 这是一个重要的清理步骤，确保资源被正确释放
    await web_surfer_agent.close()
    

if __name__ == "__main__":
    """
    程序入口点
    使用 asyncio.run() 来执行异步的 main 函数
    
    使用指南：
    1. 确保设置了正确的环境变量：
       - ENDPOINT_URL: Azure OpenAI 端点
       - DEPLOYMENT_NAME: 模型部署名称
       - AZURE_API_KEY: API 密钥
    
    2. 修改 main() 函数中的任务来执行不同的网页操作：
       - Google 搜索: "Search Google for 'your query' and summarize results"
       - 网站导航: "Navigate to website.com and find specific information"
       - 数据提取: "Go to website.com and extract contact information"
    
    3. 调整代理参数：
       - headless=True: 无界面模式，更快执行
       - headless=False: 显示浏览器，便于调试
       - animate_actions: 控制是否显示点击动画
       - max_turns: 控制最大对话轮数
    """
    asyncio.run(main())