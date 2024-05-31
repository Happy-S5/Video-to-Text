import os
from pytube import YouTube
from pydub import AudioSegment
import whisper

def download_audio(youtube_url, output_path, filename):
    try:
        yt = YouTube(youtube_url)
        audio_stream = yt.streams.get_audio_only()
        audio_path = os.path.join(output_path, f"{filename}.mp4")
        audio_stream.download(filename=audio_path)
        print(f"Downloaded audio to {audio_path}")
        return audio_path
    except Exception as e:
        print(f"Failed to download audio from {youtube_url}: {e}")
        return None

def convert_audio_to_wav(input_file, output_file):
    try:
        audio = AudioSegment.from_file(input_file)
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)  # Ensure the correct format
        audio.export(output_file, format="wav")
        print(f"Converted audio to WAV: {output_file}")
        return output_file
    except Exception as e:
        print(f"Failed to convert audio {input_file} to WAV: {e}")
        return None

def transcribe_audio_whisper(audio_path, model_size="medium"):
    try:
        model = whisper.load_model(model_size)
        result = model.transcribe(audio_path, fp16=False)  # Use fp16=False for higher precision or compatibility
        return result["text"]
    except Exception as e:
        print(f"Failed to transcribe audio {audio_path}: {e}")
        return None

def main(youtube_url, output_path, filename):
    audio_path = download_audio(youtube_url, output_path, filename)
    
    if audio_path:
        wav_path = os.path.join(output_path, f"{filename}.wav")
        wav_file = convert_audio_to_wav(audio_path, wav_path)
        
        if wav_file:
            transcription = transcribe_audio_whisper(wav_path)
          
            text_file_path = os.path.join(output_path, f"transcription_{filename}.txt")
            
            if transcription:
                with open(text_file_path, "w") as text_file:
                    text_file.write(transcription)
                print(f"Transcription saved to {text_file_path}")
            else:
                print("Transcription failed, no text to write.")
        else:
            print("Error in audio conversion.")
    else:
        print("Error in downloading audio.")

if __name__ == "__main__":
    filename = "CIA_1"
    youtube_url = "https://youtu.be/IaqazWEvRGc"
    output_path = r"C:\Users\miram\OneDrive\MIT Python Scripts\Visual S\Third"
    main(youtube_url, output_path, filename)
