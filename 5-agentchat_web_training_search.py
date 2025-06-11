"""
AutoGen Web Agent Google 搜索示例 - 包含文件保存功能
展示如何使用 AutoGen 的多模态网页浏览代理进行 Google 搜索，并使用 FileSurfer 保存结果

这个示例展示了：
1. 如何让代理在 Google 上搜索特定查询
2. 如何分析搜索结果
3. 如何提取有用的信息
4. 如何处理多个搜索任务
5. 如何使用 FileSurfer 代理将搜索结果保存到本地文件
6. 如何创建结构化的报告和分析文档
"""

# 导入必要的 AutoGen 模块
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_ext.agents.file_surfer import FileSurfer

import asyncio
import os
from datetime import datetime


def create_output_directory(dir_name: str = "search_results"):
    """
    创建输出目录（如果不存在）
    
    Args:
        dir_name: 目录名称，默认为 "search_results"
    
    Returns:
        str: 创建的目录路径
    """
    import os
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print(f"📁 创建输出目录: {dir_name}")
    else:
        print(f"📁 使用现有目录: {dir_name}")
    
    return dir_name


def setup_azure_client():
    """
    设置 Azure OpenAI 客户端
    """
    # 配置 Azure OpenAI 连接参数
    endpoint = os.getenv("ENDPOINT_URL", "https://ai-<endpoint>.openai.azure.com/")
    deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4.1")
    api_key = os.getenv("AZURE_API_KEY")
    
    # 检查必要的环境变量
    if not api_key:
        raise ValueError("AZURE_API_KEY 环境变量必须设置")
    
    # 创建并返回模型客户端
    return AzureOpenAIChatCompletionClient(
        model=deployment,
        azure_deployment=deployment,
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version="2024-12-01-preview"
    )


async def google_search_demo():
    """
    Google 搜索演示函数
    展示如何使用网页代理进行搜索和信息提取，并保存结果到本地文件
    """
    # 设置模型客户端
    model_client = setup_azure_client()
    
    # 创建网页浏览代理
    web_surfer_agent = MultimodalWebSurfer(
        name="GoogleSearchAgent",  # 给代理一个描述性的名称
        model_client=model_client,
        headless=False,  # 显示浏览器窗口，方便观察
        animate_actions=True  # 显示动画效果
    )
    
    # 创建文件操作代理
    file_surfer_agent = FileSurfer(
        name="FileManagerAgent",  # 文件管理代理
        model_client=model_client
    )
    
    # 创建包含两个代理的团队
    agent_team = MagenticOneGroupChat(
        [web_surfer_agent, file_surfer_agent],
        max_turns=25,  # 增加轮数以处理搜索和文件操作
        model_client=model_client
    )    
    # 创建输出目录
    output_dir = create_output_directory("search_results")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        # 任务 1: 基础 Google 搜索并保存结果
        print("🔍 开始执行任务 1: AI 代理培训搜索from courseare")
        search_task_1 = f"""
        Go to https://www.coursera.org and search for 'AI Agent Trainings'. 
        Look at the first 5 search results and provide a detailed summary of what each result offers.
        
        After gathering the search results, save the summary to table format, the table include:
        Include:
        - AI Agents Training title
        - URL of the title
        - Date and time of search
        - Detailed summary of each result (title, URL, description)
        - Score and ranking based on relevance and quality
        """
        
        stream_1 = agent_team.run_stream(task=search_task_1)
        await Console(stream_1)
        
        print("\n" + "="*50 + "\n")


        # 任务 2: 基础 Google 搜索并保存结果
        print("🔍 开始执行任务 2: AI 代理培训搜索from deeplearning.ai")
        search_task_2 = f"""
        Go to https://www.deeplearning.ai and search for 'AI Agent Trainings'. 
        Look at the first 5 search results and provide a detailed summary of what each result offers.
        
        After gathering the search results, save the summary to table format, the table include:
        Include:
        - AI Agents Training title
        - URL of the title
        - Date and time of search
        - Detailed summary of each result (title, URL, description)
        - Score and ranking based on relevance and quality
        """
        
        stream_2 = agent_team.run_stream(task=search_task_2)
        await Console(stream_2)
        
        print("\n" + "="*50 + "\n")
        
        # 任务 2: 技术比较搜索并保存结果
        print("🔍 开始执行任务 3: AI Agents 比较分析")
        search_task_3 = f"""
        Based on the results from the first and second searches, find and compare different AI agent training programs.
        Create a comparison table with scores and rankings for different training programs.

        Save the comparison analysis to a table format.
        Include:
        - Comparison criteria
        - Detailed scoring methodology
        - Ranking table of training programs
        - Pros and cons for each program
        - Final recommendations
        """

        stream_3 = agent_team.run_stream(task=search_task_3)
        await Console(stream_3)
        
        print("\n" + "="*50 + "\n")
        
        # 任务 3: 创建汇总报告
        print("📄 创建汇总报告")
        summary_task = f"""
        Create a comprehensive summary report that combines the results from both searches.
        
        The report should include:
        - Executive Summary
        - Detailed Findings from both searches
        - Comparison Analysis
        - Recommendations
        - Next Steps
        
        Format it professionally with proper headings, bullet points, and tables.
        """
        
        stream_3 = agent_team.run_stream(task=summary_task)
        await Console(stream_3)        
    except Exception as e:
        print(f"❌ 执行过程中出现错误: {e}")
    
    finally:
        # 确保关闭浏览器
        print("🔒 正在关闭浏览器...")
        await web_surfer_agent.close()
        print("✅ 所有搜索任务完成！搜索结果已保存到本地文件。")


async def targeted_search(query: str, additional_instructions: str = ""):
    """
    执行针对性搜索的辅助函数，并保存结果到本地文件
    
    Args:
        query: 搜索查询字符串
        additional_instructions: 额外的指令
    """
    model_client = setup_azure_client()
    
    # 创建网页浏览代理
    web_surfer_agent = MultimodalWebSurfer(
        name="TargetedSearchAgent",
        model_client=model_client,
        headless=True,  # 静默模式，更快执行
        animate_actions=False
    )
    
    # 创建文件操作代理
    file_surfer_agent = FileSurfer(
        name="FileManagerAgent",
        model_client=model_client
    )
    
    # 创建代理团队
    agent_team = MagenticOneGroupChat(
        [web_surfer_agent, file_surfer_agent],
        max_turns=20,
        model_client=model_client
    )
      # 创建输出文件名
    output_dir = create_output_directory("search_results")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_query = "".join(c for c in query if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_query = safe_query.replace(' ', '_')[:50]  # 限制文件名长度
    filename = f"{output_dir}/targeted_search_{safe_query}_{timestamp}.txt"
    
    # 构建完整的搜索任务，包含文件保存指令
    full_task = f"""
    Go to Google and search for '{query}'. {additional_instructions}
    
    After completing the search and analysis, save the results to a file named '{filename}'.
    Include in the file:
    - Search query: {query}
    - Search timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    - Additional instructions: {additional_instructions}
    - Detailed search results and analysis
    - Your conclusions and recommendations
    """
    
    try:
        print(f"🔍 执行搜索: {query}")
        print(f"📁 结果将保存到: {filename}")
        stream = agent_team.run_stream(task=full_task)
        await Console(stream)
        print(f"✅ 搜索完成，结果已保存到 {filename}")
    finally:
        await web_surfer_agent.close()


async def main():
    """
    主函数 - 选择运行模式
    """
    print("🌟 AutoGen Google 搜索代理演示 - 包含文件保存功能")
    print("=" * 50)
    print("功能特点：")
    print("✅ Google 搜索和结果分析")
    print("✅ 自动保存搜索结果到本地文件")
    print("✅ 生成结构化报告（TXT 和 Markdown 格式）")
    print("✅ 支持自定义搜索查询")
    print("=" * 50)
    
    # 可以选择运行完整演示或单个搜索
    mode = input("选择模式 (1: 完整演示, 2: 单个搜索, 3: 查看已保存文件): ").strip()
    
    if mode == "1":
        await google_search_demo()
    elif mode == "2":
        query = input("输入搜索查询: ").strip()
        instructions = input("输入额外指令 (可选): ").strip()
        await targeted_search(query, instructions)
    elif mode == "3":
        show_saved_files()
    else:
        print("无效选择，运行完整演示...")
        await google_search_demo()


def show_saved_files():
    """
    显示已保存的搜索结果文件
    """
    import os
    import glob
    
    output_dir = "search_results"
    if not os.path.exists(output_dir):
        print(f"❌ 目录 '{output_dir}' 不存在。")
        return
    
    # 查找所有保存的文件
    txt_files = glob.glob(f"{output_dir}/*.txt")
    md_files = glob.glob(f"{output_dir}/*.md")
    
    if not txt_files and not md_files:
        print(f"📁 目录 '{output_dir}' 中没有找到保存的文件。")
        return
    
    print(f"📁 在 '{output_dir}' 目录中找到以下文件：")
    print("-" * 40)
    
    if txt_files:
        print("📄 文本文件 (.txt):")
        for file in sorted(txt_files):
            file_size = os.path.getsize(file)
            mod_time = os.path.getmtime(file)
            mod_time_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
            print(f"  • {os.path.basename(file)} ({file_size} 字节, {mod_time_str})")
    
    if md_files:
        print("📝 Markdown 文件 (.md):")
        for file in sorted(md_files):
            file_size = os.path.getsize(file)
            mod_time = os.path.getmtime(file)
            mod_time_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
            print(f"  • {os.path.basename(file)} ({file_size} 字节, {mod_time_str})")
    
    print("-" * 40)
    print(f"📊 总计: {len(txt_files)} 个 TXT 文件, {len(md_files)} 个 MD 文件")


if __name__ == "__main__":
    """
    程序入口点
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断了程序执行")
    except Exception as e:
        print(f"❌ 程序执行失败: {e}")
