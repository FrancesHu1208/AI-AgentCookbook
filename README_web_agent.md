# AutoGen 网页浏览代理使用指南 - FileSurfer 集成版

这个目录包含了使用 AutoGen 框架创建智能网页浏览代理的示例代码，现在集成了 **FileSurfer 代理**来自动保存搜索结果到本地文件。

## 🆕 新功能特点

### 🤝 多代理协作

- **WebSurfer 代理**: 负责网页浏览、搜索和内容分析
- **FileSurfer 代理**: 负责文件创建、写入和管理
- **智能协作**: 两个代理无缝配合完成搜索和保存任务

### 💾 自动文件保存

- 搜索结果自动保存为结构化文件
- 支持多种格式: TXT, Markdown, JSON
- 时间戳命名，避免文件冲突
- 自动创建输出目录

## 文件说明

### 核心文件

- `agentchat_web.py` - 基础的网页浏览代理示例
- `agentchat_web_google_search.py` - **Google 搜索专用代理 + FileSurfer 集成**
- `run_search_demo.py` - **交互式演示启动器**
- `test_file_saving.py` - FileSurfer 功能测试脚本

### 辅助文件

- `run_demo.ps1` - PowerShell 启动脚本
- `.env.template` - 环境变量配置模板
- `.env.example` - 环境变量示例文件

## 快速开始

### 1. 安装依赖

```bash
pip install autogen-agentchat autogen-ext python-dotenv
```

### 2. 配置环境

复制 `.env.template` 为 `.env` 并填入配置：

```bash
ENDPOINT_URL=https://your-resource.openai.azure.com/
DEPLOYMENT_NAME=gpt-4
AZURE_API_KEY=your_api_key_here
```

### 3. 运行演示

**推荐方式 - PowerShell 启动器:**

```powershell
.\run_demo.ps1
```

**或者直接运行 Python 脚本:**

```bash
python run_search_demo.py
```

## 主要功能

### 🔍 智能搜索

- Google 搜索和结果分析
- 自动提取关键信息
- 多种搜索策略支持

### 📝 自动文档生成

- 结构化搜索报告
- Markdown 格式输出
- 比较分析表格
- 时间戳和元数据

### 🔄 批量处理

- 支持批量搜索多个相关查询
- 预设技术话题快速搜索
- 自定义搜索任务

## 使用示例

### 基础搜索

```python
# 搜索并保存结果
query = "Python machine learning tutorials"
await targeted_search(query, "Focus on practical examples")
```

### 完整演示

```python
# 运行完整的 AI 代理培训搜索演示
await google_search_demo()
```

## 输出文件格式

### 搜索结果文件

- `search_results/ai_agent_trainings_20240608_143052.txt`
- `search_results/ai_agent_comparison_20240608_143052.txt`
- `search_results/ai_training_complete_report_20240608_143052.md`

### 文件内容结构

每个文件包含：

- 搜索查询和时间戳
- 详细的搜索结果分析
- 结构化的比较表格
- 建议和结论

## 高级功能

### 多代理协作示例

```python
# 创建代理团队
web_surfer_agent = MultimodalWebSurfer(...)
file_surfer_agent = FileSurfer(...)
agent_team = MagenticOneGroupChat([web_surfer_agent, file_surfer_agent])

# 执行搜索和保存任务
task = "Search and save results to file"
stream = agent_team.run_stream(task=task)
```

### 自定义文件格式

代理支持保存为多种格式：

- TXT: 纯文本报告
- Markdown: 格式化文档
- JSON: 结构化数据

## 故障排除

### 常见问题

1. **环境变量未设置**
   - 确保 `.env` 文件配置正确
   - 检查 Azure OpenAI 服务访问权限

2. **文件保存失败**
   - 确保有足够的磁盘空间
   - 检查文件路径权限

3. **代理执行超时**
   - 增加 `max_turns` 参数
   - 简化搜索任务描述

### 调试技巧

- 使用 `headless=False` 观察浏览器操作
- 检查控制台输出查看详细日志
- 查看 `search_results` 目录中的输出文件

## 贡献指南

欢迎提交改进建议和 Bug 报告！

**注意**: 使用时请遵守相关网站的使用条款和法律法规。
