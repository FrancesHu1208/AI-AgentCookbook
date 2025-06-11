from openai import AzureOpenAI
import json
from openai.types.chat import ChatCompletionUserMessageParam, ChatCompletionSystemMessageParam
import os
import base64
import requests
import azure.cognitiveservices.speech as speechsdk
import pygame
import io
import tempfile
import re
import time
from dotenv import load_dotenv
import re
import time
from pydub import AudioSegment
from pydub.playback import play
import pyglet

# Load environment variables
load_dotenv()

query = "今天的北京的天气如何?"

def send_reply(message: str, enable_speech=True):
    """
    发送回复并可选择播放语音
    
    Args:
        message (str): 要发送的消息
        enable_speech (bool): 是否启用语音播放
    """
    print(f"🤖 Reply: {message}")
    
    if enable_speech:
        print("🔊 Converting to speech...")
        success = text_to_speech(message)
        if not success:
            print("⚠️  Speech playback failed, continuing with text only...")
    
    return message

def get_weather(latitude, longitude):
    """
    从Open-Meteo API获取天气数据
    """
    try:
        response = requests.get(
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}&longitude={longitude}"
            f"&current=temperature_2m,wind_speed_10m,relative_humidity_2m,weather_code"
            f"&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
        )
        response.raise_for_status()
        data = response.json()
        
        current = data['current']
        return {
            'temperature': current['temperature_2m'],
            'wind_speed': current['wind_speed_10m'],
            'humidity': current.get('relative_humidity_2m', 'N/A'),
            'weather_code': current.get('weather_code', 0)
        }
    except requests.RequestException as e:
        print(f"❌ Error fetching weather data: {e}")
        return None

def detect_language(text):
    """
    检测文本语言 (简单的中英文检测)
    """
    # 计算中文字符比例
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    total_chars = len(text.strip())
    
    if total_chars == 0:
        return "en-US"
    
    chinese_ratio = chinese_chars / total_chars
    return "zh-CN" if chinese_ratio > 0.1 else "en-US"

def text_to_speech(text, language=None):
    """
    将文本转换为语音并播放
    支持中英文语音合成，自动语言检测
    
    Args:
        text (str): 要转换的文本
        language (str, optional): 指定语言，如果不指定则自动检测
    
    Returns:
        bool: 成功返回True，失败返回False
    """
    # Azure Speech Service 配置
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION", "eastus2")
    
    if not speech_key:
        print("❌ Azure Speech Service key not found. Please set AZURE_SPEECH_KEY environment variable.")
        print("📝 You can get a key from: https://portal.azure.com -> Cognitive Services -> Speech")
        print("💡 Copy .env.template to .env and add your Speech Service key")
        return False
    
    # 自动检测语言或使用指定语言
    if language is None:
        language = detect_language(text)
    
    try:
        # 根据语言选择语音
        voice_map = {
            "zh-CN": "zh-CN-XiaoxiaoNeural",  # 中文女声 (温柔)
            "en-US": "en-US-JennyNeural",     # 英文女声 (友好)
            "en-GB": "en-GB-SoniaNeural",     # 英式英语女声
        }
        
        voice_name = voice_map.get(language, "en-US-JennyNeural")
        
        # 配置语音服务
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        speech_config.speech_synthesis_voice_name = voice_name
        speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
        )
        
        # 创建临时文件存储音频
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_filename = temp_file.name
            temp_file.close()
        
        # 配置音频输出到文件
        audio_config = speechsdk.audio.AudioOutputConfig(filename=temp_filename)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        
        print(f"🔊 Converting text to speech: {text[:50]}{'...' if len(text) > 50 else ''}")
        print(f"🎵 Language: {language}, Voice: {voice_name}")
        
        # 合成语音
        try:
            result = synthesizer.speak_text_async(text).get()

            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted: # type: ignore
                print("✅ Speech synthesis completed successfully!")
                audio_stream = speechsdk.AudioDataStream(result)
                audio_stream.save_to_wav_file("C:\\Users\\OneDrive - Microsoft\\Technical\\Copilot\\file.wav")

                p = pyglet.media.Player()
                source = pyglet.media.load("C:\\Users\\OneDrive - Microsoft\\Technical\\Copilot\\file.wav")
                p.queue(source)
                p.play()
                pyglet.app.run()
            else:
                print("Speech synthesis failed.")
            return True
        finally:
            # 清理临时文件
            try:
                os.unlink(temp_filename)
            except OSError:
                pass

    except Exception as e:
        print(f"❌ Error in text-to-speech: {e}")
        if "No module named" in str(e):
            print("💡 Try running: pip install azure-cognitiveservices-speech pygame")
        return False


endpoint = os.getenv("ENDPOINT_URL", "https://<endpoint>.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4.1")
api_key = os.getenv("AZURE_API_KEY")

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2025-01-01-preview",
)

# --------------------------------------------------------------
# Structured output example using function calling
# --------------------------------------------------------------

# --------------------------------------------------------------
# Structured output example using function calling with voice output
# --------------------------------------------------------------

def main():
    """
    主函数：演示天气查询功能与语音播放
    """
    print("🌤️  Weather Assistant with Voice Output")
    print("=" * 50)
    # 可以通过环境变量或参数设置
    
    enable_speech = os.getenv("ENABLE_SPEECH", "true").lower() == "true"

    print(f"📝 Query: {query}")
    print(f"🔊 Speech enabled: {enable_speech}")
    print("-" * 50)
    
    function_name = "get_weather"

    # 定义用于获取指定经纬度天气的函数
    tools = [{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取所提供坐标的当前天气信息，包括温度、湿度、风速等。",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number", "description": "纬度"},
                    "longitude": {"type": "number", "description": "经度"},
                    "location": {
                        "type": "string",
                        "description": "地点名称，例如城市或地区",
                        "example": "Shanghai"
                    }
                },
                "required": ["latitude", "longitude", "location"],
                "additionalProperties": False
            }
        }
    }]

    messages = [
        ChatCompletionSystemMessageParam(
            role="system",
            content="You're a helpful weather assistant that can get weather information and provide friendly responses. Always respond in the same language as the user's query.",
        ),
        ChatCompletionUserMessageParam(
            role="user",
            content=query,
        ),
    ]

    try:
        print("🤖 Calling OpenAI API...")
        response = client.chat.completions.create(
            model=deployment,
            messages=messages,
            tools=tools, # type: ignore
            tool_choice={"type": "function", "function": {"name": function_name}},
        )

        if not response.choices[0].message.tool_calls:
            print("❌ No tool calls received from API")
            return

        tool_call = response.choices[0].message.tool_calls[0]
        function_args = json.loads(tool_call.function.arguments)
        
        print(f"📍 Location: {function_args['location']}")
        print(f"🌐 Coordinates: {function_args['latitude']}, {function_args['longitude']}")
        
        # 获取天气数据
        print("🌤️  Fetching weather data...")
        weather_data = get_weather(function_args["latitude"], function_args["longitude"])
        
        if weather_data is None:
            error_msg = f"Sorry, I couldn't get the weather data for {function_args['location']}. Please try again later."
            send_reply(error_msg, enable_speech)
            return
        
        location = function_args['location']
        
        # 构建详细的天气报告
        if "中" in query or detect_language(query) == "zh-CN":
            # 中文回复
            weather_report = f"{location}的当前天气：温度 {weather_data['temperature']}°C"
            if weather_data['humidity'] != 'N/A':
                weather_report += f"，湿度 {weather_data['humidity']}%"
            weather_report += f"，风速 {weather_data['wind_speed']} km/h。"
        else:
            # 英文回复
            weather_report = f"Current weather in {location}: {weather_data['temperature']}°C"
            if weather_data['humidity'] != 'N/A':
                weather_report += f", humidity {weather_data['humidity']}%"
            weather_report += f", wind speed {weather_data['wind_speed']} km/h."
        
        # 发送回复并播放语音
        send_reply(weather_report, enable_speech)
        
        print("\n✅ Weather query completed successfully!")
        
    except json.JSONDecodeError as e:
        error_msg = f"Error parsing function arguments: {e}"
        print(f"❌ {error_msg}")
        send_reply("Sorry, there was an error processing your request.", enable_speech)
        
    except Exception as e:
        error_msg = f"An unexpected error occurred: {e}"
        print(f"❌ {error_msg}")
        send_reply("Sorry, I'm having trouble getting the weather information right now.", enable_speech)

if __name__ == "__main__":
    main()