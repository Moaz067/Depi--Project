import pyttsx3
import os
from datetime import datetime

# Read the text file
def read_script_file(file_path):
    """
    Read text from a file
    
    Args:
        file_path: Path to the text file
        
    Returns:
        The content of the file as a string
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def text_to_speech(text, rate=150, volume=1.0, voice_gender='male', save_to_file="data/voices", auto_name=True):
    """
    Convert text to speech using pyttsx3
    
    Args:
        text: The text to convert to speech
        rate: Speech rate (words per minute), default 150
        volume: Volume level (0.0 to 1.0), default 1.0
        voice_gender: 'male' or 'female', default 'male'
        save_to_file: Path to save audio (can be folder or full path)
        auto_name: If True and save_to_file is a folder, generates unique filename
    """
    # Initialize the TTS engine
    engine = pyttsx3.init()
    
    # Set properties
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    
    # Set voice based on gender
    voices = engine.getProperty('voices')
    if voice_gender.lower() == 'female':
        # Try to find a female voice
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        else:
            # If no female voice found, use index 1
            if len(voices) > 1:
                engine.setProperty('voice', voices[1].id)
    else:
        # Male voice
        if len(voices) > 0:
            engine.setProperty('voice', voices[0].id)
    
    # Save to file if specified
    if save_to_file:
        # If save_to_file is a directory, generate a unique filename
        if auto_name and (os.path.isdir(save_to_file) or not save_to_file.endswith('.wav')):
            # Create directory if it doesn't exist
            if not os.path.exists(save_to_file):
                os.makedirs(save_to_file)
            
            # Generate unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"voice_{timestamp}.wav"
            save_to_file = os.path.join(save_to_file, filename)
        else:
            # Create directory for the file if it doesn't exist
            directory = os.path.dirname(save_to_file)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # Ensure the file has .wav extension
            if not save_to_file.endswith('.wav'):
                save_to_file = save_to_file + '.wav'
        
        engine.save_to_file(text, save_to_file)
        engine.runAndWait()
        print(f"Audio saved to {save_to_file}")
        return save_to_file
    else:
        # Speak the text
        engine.say(text)
        engine.runAndWait()
        return None

# Example usage
if __name__ == "__main__":
    text = "Hello! This is a text to speech conversion example."
    
    # Speak with male voice
    # text_to_speech(text, voice_gender='male')
    
    # Speak with female voice
    # text_to_speech(text, voice_gender='female')
    
    # Save to folder with male voice
    # text_to_speech(text, voice_gender='male', save_to_file="data/voices")
    
    # Save to folder with female voice
    # text_to_speech(text, voice_gender='female', save_to_file="data/voices")

    my_text = read_script_file("data\scripts\script_20251120_235857.txt")
    text_to_speech(my_text, voice_gender="male", save_to_file="data/voices")
    
    # Or save with specific filename
    # text_to_speech(text, voice_gender='female', save_to_file="data/voices/female_speech.wav", auto_name=False)