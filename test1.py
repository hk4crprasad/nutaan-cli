import azure.cognitiveservices.speech as speechsdk

# Your Azure Speech credentials
speech_key = "6G5ZtFhP3ArtJ8XfAeaY143eoXt5h3vMuQsytiIYmf3CO03YT5CcJQQJ99BDACYeBjFXJ3w3AAAAACOG9tTT"
service_region = "eastus"

# Create the speech configuration
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Set desired voice
speech_config.speech_synthesis_voice_name = "en-US-BrandonMultilingualNeural"

# Set output format to MP3
speech_config.set_speech_synthesis_output_format(
    speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
)

# Output filename (MP3)
audio_config = speechsdk.audio.AudioOutputConfig(filename="output.mp3")

# Create the synthesizer
speech_synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config, audio_config=audio_config
)

# Text to convert
text = """Hi, Priya. You don’t look too well. Are you okay?
Hi, Alex. Not really. I’ve been feeling sick since last night.

Oh no, what’s wrong?
I have a terrible headache and my throat hurts a lot. I also feel really tired.

That sounds rough. Did it start suddenly?
Yes, it hit me last night. I couldn’t sleep properly and woke up feeling weak.

You should definitely see someone about it. Could be an infection.
Yeah, I was thinking the same. I just don’t know where to go.

There’s a good clinic not far from here. I’ve been there once. Want the address?
That would be great. Thanks. Actually… would you mind coming with me?

Of course. Happy to help. Do you know exactly what symptoms you have?
So far, fever, headache, throat pain, and extreme fatigue.

Those are important signs. When we get there, the doctor will probably ask about your symptoms and how long you've had them.
Okay, good to know. I just hope it’s nothing serious.

Better to get checked early than wait and risk it.
Should I bring anything with me to the clinic?

Yes, take your ID, any medical documents you have, and any medications you're currently taking.
Got it. Also… I don’t speak the local language very well. Should I mention that?

Definitely. It’s important. Most clinics have someone who can translate or help you in English.
That makes me feel better. How long do you think the appointment will take?

Depends on how busy it is, but usually not more than 20–30 minutes. If possible, booking ahead can save time.
Yeah, I’d prefer not to wait too long. When I meet the doctor, what should I say?

Just explain your symptoms clearly: say you have a headache, sore throat, fever, and fatigue. Also tell them when it started.
Okay, I’ll try to remember all that. I’m just a bit nervous.

Don’t worry, you’re not alone. I’ll be with you. Is there anything else you’re unsure about?
I guess… what questions should I ask the doctor?

Ask about the cause, what treatment they suggest, how long recovery might take, and if you need to rest or take any precautions at home.
That’s helpful. Thanks for walking me through this.

No problem, Priya. That’s what friends are for. Ready to head out now?
Yes, please. I’m really not feeling up to driving myself.

Alright, let’s go. After the appointment, we’ll stop at the pharmacy and get what you need.
Thank you, Alex. I really appreciate you being here.

Always. Let’s get you feeling better soon."""

# Synthesize speech to MP3 file
result = speech_synthesizer.speak_text_async(text).get()

# Check result
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("✅ Speech synthesized and saved as 'output.mp3'")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation = result.cancellation_details
    print("❌ Speech synthesis canceled: {}".format(cancellation.reason))
    if cancellation.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation.error_details))
