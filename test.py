import azure.cognitiveservices.speech as speechsdk
import requests
import uuid
import json
from pydub import AudioSegment
import os
import time

# ---------- CONFIG ----------
speech_key = "6G5ZtFhP3ArtJ8XfAeaY143eoXt5h3vMuQsytiIYmf3CO03YT5CcJQQJ99BDACYeBjFXJ3w3AAAAACOG9tTT"
speech_region = "eastus"
translator_key = speech_key
translator_region = speech_region

mp3_path = "/home/cp/LangTests/output.mp3"
wav_path = "temp_audio.wav"

# ---------- Convert MP3 to WAV ----------
print("🔄 Converting MP3 to WAV...")
audio = AudioSegment.from_mp3(mp3_path)
audio = audio.set_channels(1).set_frame_rate(16000)
audio.export(wav_path, format="wav")
print("✅ Conversion complete.")

# ---------- Continuous STT ----------
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
speech_config.speech_recognition_language = "ar-EG"
audio_input = speechsdk.audio.AudioConfig(filename=wav_path)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

print("🗣️ Starting full audio recognition...")

recognized_text = []

def handle_result(evt):
    if evt.result.text:
        print("→", evt.result.text)
        recognized_text.append(evt.result.text)

speech_recognizer.recognized.connect(handle_result)

done = False

def stop_cb(evt):
    global done
    done = True

speech_recognizer.session_stopped.connect(stop_cb)
speech_recognizer.canceled.connect(stop_cb)

speech_recognizer.start_continuous_recognition()
while not done:
    time.sleep(0.5)
speech_recognizer.stop_continuous_recognition()

# ---------- Combine all recognized lines ----------
arabic_full_text = " ".join(recognized_text)
print(f"\n✔️ Full Arabic Recognized:\n{arabic_full_text}")

# ---------- Translation ----------
print("\n🌐 Translating Arabic to English...")
endpoint = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from=ar&to=en"
headers = {
    "Ocp-Apim-Subscription-Key": translator_key,
    "Ocp-Apim-Subscription-Region": translator_region,
    "Content-type": "application/json",
    "X-ClientTraceId": str(uuid.uuid4())
}
body = [{"text": arabic_full_text}]
response = requests.post(endpoint, headers=headers, json=body)
result = response.json()
english_translation = result[0]['translations'][0]['text']
print(f"\n🔁 English Translation:\n{english_translation}")

# ---------- Cleanup ----------
if os.path.exists(wav_path):
    os.remove(wav_path)
