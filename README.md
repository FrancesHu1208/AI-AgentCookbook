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


### 🔍 Advanced Search Capabilities

- **Multi-Platform Search**: Searches across Coursera, DeepLearning.ai, and general Google results
- **Targeted Queries**: Specialized search for AI Agent training courses and resources
- **Content Analysis**: Extracts key information including pricing, ratings, difficulty levels
- **Metadata Collection**: Captures comprehensive course details and technical specifications

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





## 📞 Support

For questions and support:

- Check the existing documentation in `README_web_agent.md`
- Review the example code in the templates directory
- Open an issue for bugs or feature requests
