# Weather Assistant with Voice Output 🌤️🔊

A sophisticated weather application that combines OpenAI's function calling capabilities with Azure Speech Services to provide spoken weather reports in multiple languages.

## Features ✨

- **🌍 Multi-language Support**: Automatic language detection for Chinese and English
- **🎵 High-Quality Voice Synthesis**: Azure Neural Voices for natural-sounding speech
- **🤖 AI-Powered**: Uses OpenAI GPT for intelligent weather queries
- **📍 Location-Aware**: Automatically extracts coordinates from city names
- **🔊 Audio Playback**: Real-time voice output using pygame
- **⚡ Error Handling**: Robust error handling with helpful user guidance

## Setup Instructions 🚀

### 1. Install Dependencies

```bash
pip install -r speech_requirements.txt
```

Required packages:
- `azure-cognitiveservices-speech` - Azure Speech SDK
- `pygame` - Audio playback
- `python-dotenv` - Environment variable loading
- `requests` - HTTP requests

### 2. Configure Azure Services

#### Azure Speech Service
1. Go to [Azure Portal](https://portal.azure.com)
2. Create a new **Cognitive Services** → **Speech** resource
3. Copy the **Key** and **Region** from your Speech resource

#### Azure OpenAI Service
1. Ensure you have access to Azure OpenAI Service
2. Note your **Endpoint URL**, **API Key**, and **Deployment Name**

### 3. Environment Configuration

Copy the template file and configure your credentials:

```bash
cp .env.template .env
```

Edit `.env` file:
```bash
# Azure OpenAI Configuration
ENDPOINT_URL=https://your-openai-resource.openai.azure.com/
DEPLOYMENT_NAME=gpt-4
AZURE_API_KEY=your_azure_openai_api_key_here

# Azure Speech Service Configuration
AZURE_SPEECH_KEY=your_azure_speech_service_key_here
AZURE_SPEECH_REGION=eastus

# Optional: Customize default query and settings
WEATHER_QUERY=今天上海的天气怎么样？
ENABLE_SPEECH=true
```

## Usage 🎯

### Basic Weather Query

```bash
python 03-function-calling-weather.py
```

### Voice Demo

Test different voice capabilities:

```bash
python voice_demo.py
```

### Quick Start Scripts

**Windows Batch:**
```bash
start_weather_voice.bat
```

**PowerShell:**
```bash
.\start_weather_voice.ps1
```

## Voice Models and Languages 🗣️

### Supported Voices

| Language | Voice Model | Gender | Style |
|----------|-------------|--------|-------|
| Chinese (Simplified) | `zh-CN-XiaoxiaoNeural` | Female | Gentle, friendly |
| English (US) | `en-US-JennyNeural` | Female | Friendly, conversational |
| English (UK) | `en-GB-SoniaNeural` | Female | Clear, professional |

### Language Detection

The application automatically detects the input language:
- **Chinese**: Detected when >10% of characters are Chinese
- **English**: Default for other languages

### Custom Voice Configuration

You can modify the voice selection in the `text_to_speech()` function:

```python
voice_map = {
    "zh-CN": "zh-CN-XiaoxiaoNeural",  # Chinese female
    "en-US": "en-US-JennyNeural",     # US English female
    "en-GB": "en-GB-SoniaNeural",     # UK English female
}
```

## Code Structure 📁

```
04-structured-output/
├── 03-function-calling-weather.py  # Main weather app with voice
├── voice_demo.py                   # Voice capability demonstration
├── speech_requirements.txt         # Python dependencies
├── .env.template                   # Environment variable template
├── .env.example                    # Example configuration
├── start_weather_voice.bat         # Windows startup script
├── start_weather_voice.ps1         # PowerShell startup script
└── README.md                       # This file
```

## Key Functions 🔧

### `text_to_speech(text, language=None)`
Converts text to speech with automatic language detection.

**Parameters:**
- `text` (str): Text to convert to speech
- `language` (str, optional): Force specific language ("zh-CN", "en-US")

**Returns:**
- `bool`: True if successful, False otherwise

### `detect_language(text)`
Automatically detects text language based on character analysis.

### `get_weather(latitude, longitude)`
Fetches comprehensive weather data from Open-Meteo API.

**Returns:**
- Dictionary with temperature, humidity, wind speed, and weather code

## Example Queries 💬

### English Queries
- "What's the weather like in New York today?"
- "How is the weather in London?"
- "Tell me about the weather in Tokyo"

### Chinese Queries
- "今天上海的天气怎么样？"
- "北京现在的天气如何？"
- "深圳今天的天气情况"

## Troubleshooting 🔧

### Common Issues

**1. "Azure Speech Service key not found"**
- Check your `.env` file exists and contains `AZURE_SPEECH_KEY`
- Verify the key is correct and not the placeholder text

**2. "No module named 'pygame'"**
```bash
pip install pygame
```

**3. "Speech synthesis canceled: Error"**
- Check your Azure Speech Service key and region
- Ensure your Azure subscription is active
- Verify the region matches your Speech resource

**4. Audio not playing**
- Check your system audio settings
- Ensure pygame can access audio devices
- Try running with administrator privileges

### Testing Speech Service

Test your Azure Speech Service configuration:

```python
python -c "
import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('AZURE_SPEECH_KEY')
region = os.getenv('AZURE_SPEECH_REGION')

print(f'Key: {key[:10]}...' if key else 'No key found')
print(f'Region: {region}')
"
```

## Advanced Configuration ⚙️

### Custom Weather Queries

Set environment variables for different default queries:

```bash
# Chinese weather query
export WEATHER_QUERY="今天广州的天气怎么样？"

# English weather query  
export WEATHER_QUERY="What's the weather like in San Francisco today?"

# Disable speech output
export ENABLE_SPEECH=false
```

### Audio Quality Settings

Modify audio settings in `text_to_speech()`:

```python
# High quality audio
speech_config.set_speech_synthesis_output_format(
    speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm
)

# Lower latency
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=256)
```

## Performance Tips 🚀

1. **Faster Audio Playback**: Use smaller buffer sizes for lower latency
2. **Caching**: Consider caching frequently used audio clips
3. **Async Processing**: For multiple queries, consider async audio processing
4. **Regional Optimization**: Use the Azure region closest to your location

## License and Credits 📄

This project demonstrates Azure AI services integration. Make sure to comply with:
- Azure Terms of Service
- OpenAI Usage Policies  
- Open-Meteo API Terms

## Support 🤝

For issues related to:
- **Azure Speech Service**: [Azure Support](https://azure.microsoft.com/support/)
- **OpenAI API**: [OpenAI Support](https://help.openai.com/)
- **Code Issues**: Check the troubleshooting section above

---

**🎉 Enjoy your voice-enabled weather assistant!**
