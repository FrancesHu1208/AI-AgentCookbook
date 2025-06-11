# AI Agent Basic Sample Code Repository

A comprehensive demonstration of the AutoGen framework showcasing intelligent web browsing agents. This project combines the power of AutoGen's multi-modal web surfing agents with structured data output to Excel files.

## 🌟 Project Overview

This repository contains advanced examples of AutoGen agents that can:

- **Intelligently browse the web** using MultimodalWebSurfer agents
- **Search and analyze content** from multiple sources (Coursera, DeepLearning.ai, Google)
- **Automatically save results** to structured Excel files using pandas
- **Generate comparative analysis** across different platforms
- **Create comprehensive reports** with scoring and recommendations

## 🚀 Key Features

### 🤖 Multi-Agent Collaboration

- **WebSurfer Agent**: Handles web browsing, searching, and content analysis
- **FileSurfer Agent**: Manages file operations and Excel creation
- **Intelligent Coordination**: Seamless collaboration between agents for complex tasks

### 📊 Excel Integration & Analytics

- **Automated Excel Generation**: Creates professionally formatted Excel files with multiple worksheets
- **Structured Data Export**: Organizes search results into tables with proper formatting
- **Comparative Analysis**: Generates side-by-side comparisons between different platforms
- **Scoring Systems**: Implements custom scoring algorithms for course evaluation
- **Dashboard Creation**: Builds executive summary dashboards for quick insights

### 🔍 Advanced Search Capabilities

- **Multi-Platform Search**: Searches across Coursera, DeepLearning.ai, and general Google results
- **Targeted Queries**: Specialized search for AI Agent training courses and resources
- **Content Analysis**: Extracts key information including pricing, ratings, difficulty levels
- **Metadata Collection**: Captures comprehensive course details and technical specifications

## 📁 Project Structure

```
AI-Agent-Basic-Sample/
├── 🎯 Core Web Search Files
│   ├── agentchat_web_google_search_updated.py  # Main Excel-integrated search agent
│   ├── agentchat_web_google_search copy.py     # Original agent implementation  
│   ├── 5-agentchat_web_training_search.py      # Training-focused search demo
│   └── agentchat_web.py                        # Basic web browsing agent
│
├── 📊 Excel & Analytics
│   ├── demo_excel_features.py                  # Excel functionality demonstration
│   ├── EXCEL_UPDATE_GUIDE.md                   # Excel integration guide
│   └── search_results/                         # Output directory for Excel files
│
├── 🚀 Quick Start Scripts
│   ├── start_excel_search.bat                  # Windows batch launcher
│   ├── start_web.bat / start_web.ps1           # Web agent launchers
│   └── run_demo.ps1                            # PowerShell demo script
│
├── 🎤 Voice & Additional Features
│   ├── start_weather_voice.bat/.ps1            # Voice-enabled weather agent
│   ├── speech_requirements.txt                 # Voice feature dependencies
│   └── README_Voice.md                         # Voice features documentation
│
└── 📚 Documentation & Config
    ├── README_web_agent.md                     # Web agent detailed guide
    ├── web_requirements.txt                    # Web agent dependencies
    └── templates/                              # Agent templates and examples
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- Azure OpenAI API access
- Required Python packages (see requirements)

### Environment Configuration
Set up your Azure OpenAI credentials:
```bash
export ENDPOINT_URL="https://your-resource.openai.azure.com/"
export DEPLOYMENT_NAME="gpt-4.1"
export AZURE_API_KEY="your-api-key"
```

### Install Dependencies
```bash
pip install -r web_requirements.txt
# Additional packages for Excel functionality
pip install pandas openpyxl
```

## 🎮 Quick Start Guide

### 1. Excel-Integrated Search (Recommended)
```bash
# Windows
start_excel_search.bat

# Or run directly
python agentchat_web_google_search_updated.py
```

### 2. Basic Web Search
```bash
python 5-agentchat_web_training_search.py
```

### 3. Interactive Demo
```bash
python agentchat_web.py
```

## 💼 Use Cases & Examples

### AI Training Course Research
The main use case demonstrates comprehensive research of AI Agent training courses:

**Search Sources:**

- Coursera platform for academic courses
- DeepLearning.ai for practical training
- General Google search for additional resources

**Generated Reports:**

- Course comparison tables with scoring
- Platform analysis with strengths/weaknesses
- Learning pathway recommendations
- Cost-benefit analysis

### Custom Search Scenarios
```python
# Targeted search with custom instructions
await targeted_search(
    query="Python machine learning tutorials",
    additional_instructions="Focus on beginner-friendly content"
)
```

## 📊 Excel Output Features

### Multi-Sheet Workbooks
Each search generates comprehensive Excel files with:

**Search Summary Sheet:**

- Query details and metadata
- Search timestamp and parameters
- Total results found

**Course Details Sheet:**

- Complete course information
- Pricing, ratings, and enrollment data
- Provider and instructor details

**Analysis Sheet:**

- Custom scoring algorithms
- Relevance and quality ratings
- Recommendations and insights

**Comparison Sheet:**

- Side-by-side platform analysis
- Ranking and scoring systems
- Final recommendations

### Advanced Excel Features

- **Professional Formatting**: Auto-adjusted columns, bold headers
- **Multiple Worksheets**: Organized data structure
- **Scoring Systems**: Custom algorithms for course evaluation
- **Dashboard Views**: Executive summary perspectives

## 🔧 Technical Architecture

### Agent Framework
Built on AutoGen's multi-agent architecture:

```python
# Multi-agent setup
web_surfer_agent = MultimodalWebSurfer(...)
file_surfer_agent = FileSurfer(...)
agent_team = MagenticOneGroupChat([web_surfer_agent, file_surfer_agent])
```

### Data Processing Pipeline

1. **Web Search Execution**: Agents browse and extract content
2. **Data Structuring**: Convert web content to structured data
3. **Excel Generation**: Use pandas for professional Excel creation
4. **Analysis & Scoring**: Apply custom algorithms for evaluation
5. **Report Generation**: Create comprehensive analytical reports

### Integration Points

- **Azure OpenAI**: Powers the intelligent agents
- **Pandas**: Handles Excel file creation and data manipulation
- **AutoGen Framework**: Manages agent coordination and communication
- **Web Browsing**: Real-time content extraction and analysis

## 🚀 Advanced Features

### Custom Scoring Systems

- **Relevance Scoring**: 1-10 scale based on query match
- **Content Quality**: Assessment of course depth and structure  
- **Value Analysis**: Cost-benefit evaluation
- **Technical Depth**: For specialized technical content

### Multi-Platform Analysis

- **Coursera Integration**: Academic and professional courses
- **DeepLearning.ai Focus**: Hands-on AI/ML training
- **Google Search**: Comprehensive web coverage
- **Comparative Analytics**: Cross-platform insights

### File Management

- **Automated Organization**: Timestamped file naming
- **Directory Structure**: Organized output folders
- **Format Support**: Excel, TXT, Markdown outputs
- **Conflict Prevention**: Unique naming conventions

## 🎯 Target Audience

- **Researchers**: Academic and industry research projects
- **Data Analysts**: Market research and competitive analysis
- **Educators**: Course discovery and curriculum planning
- **Developers**: AI/ML learning path optimization
- **Business Professionals**: Training program evaluation

## 📈 Future Enhancements

- **Real-time Collaboration**: Multi-user agent coordination
- **Advanced Analytics**: Machine learning-based recommendations
- **API Integration**: Direct platform API connections
- **Visualization**: Interactive charts and graphs in Excel
- **Automation**: Scheduled searches and updates

## JSON Mode

In [JSON mode](https://platform.openai.com/docs/guides/text-generation/json-mode), the model generates outputs exclusively formatted as valid JSON strings. However, you need to explicitly specify the desired JSON structure within the system prompt to guide the model towards the expected format.

Here's an example of using JSON mode:

```python
query = "Hi there, I have a question about my bill. Can you help me?"

messages = [
    {
        "role": "system",
        "content": """
        You're a helpful customer care assistant that can classify incoming messages and create a response.
        Always response in the following JSON format: {"content": <response>, "category": <classification>}
        Available categories: 'general', 'order', 'billing'
        """,
    },
    {
        "role": "user",
        "content": query,
    },
]

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    response_format={"type": "json_object"},
)
message = response.choices[0].message.content

type(message)  # str

message_json = json.loads(message)
type(message_json)  # dict
```

It's important to note that OpenAI does not guarantee that the output text will have your specified JSON format. It only ensures that the output will be a valid string that can be parsed to JSON.

### API Reference

- `response_format`: An object specifying the format that the model must output. Compatible with GPT-4 Turbo and all GPT-3.5 Turbo models newer than gpt-3.5-turbo-1106. Setting to `{"type": "json_object"}` enables JSON mode, which guarantees the message the model generates is valid JSON.

Important: When using JSON mode, you must also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly "stuck" request. Also note that the message content may be partially cut off if `finish_reason="length"`, which indicates the generation exceeded `max_tokens` or the conversation exceeded the max context length.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **AutoGen Framework**: For providing the multi-agent architecture
- **Microsoft**: For Azure OpenAI services and tools
- **OpenAI**: For the underlying language models
- **Pandas Community**: For excellent data manipulation tools

## 📞 Support

For questions and support:

- Check the existing documentation in `README_web_agent.md`
- Review the example code in the templates directory
- Open an issue for bugs or feature requests