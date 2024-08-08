import boto3
import os

#Amazon polly credentials
polly = boto3.Session(
    aws_access_key_id='abc',
    aws_secret_access_key='xyz',
    region_name='us-east-1'
).client('polly')

# Define the new set of sentences
sentences = [
    "Please call Stella.",
    "She can scoop these things into three red bags, and we will go meet her Wednesday at the train station.",
    "When a man looks for something beyond his reach, his friends say he is looking for the pot of gold at the end of the rainbow.",
    "Some have accepted it as a miracle without physical explanation.",
    "To the Hebrews it was a token that there would be no more universal floods.",
    "The difference in the rainbow depends considerably upon the size of the drops, and the width of the colored band increases as the size of the drops increases.",
    "The rainbow is a division of white light into many beautiful colors.",
    "When the sunlight strikes raindrops in the air, they act as a prism and form a rainbow.",
    "The Norsemen considered the rainbow as a bridge over which the gods passed from earth to their home in the sky.",
    "The Greeks used to imagine that it was a sign from the gods to foretell war or heavy rain.",
    "Six spoons of fresh snow peas, five thick slabs of blue cheese, and maybe a snack for her brother Bob.",
    "Ask her to bring these things with her from the store.",
    "People look, but no one ever finds it.",
    "Since then physicists have found that it is not reflection, but refraction by the raindrops which causes the rainbows.",
    "Others have tried to explain the phenomenon physically.",
    "We also need a small plastic snake and a big toy frog for the kids.",
    "If the red of the second bow falls upon the green of the first, the result is to give a bow with an abnormally wide yellow band, since red and green light when mixed form yellow.",
    "Many complicated ideas about the rainbow have been formed.",
    "The actual primary rainbow observed is said to be the effect of super-imposition of a number of bows.",
    "These take the shape of a long round arch, with its path high above, and its two ends apparently beyond the horizon.",
    "Throughout the centuries people have explained the rainbow in various ways.",
    "Aristotle thought that the rainbow was caused by reflection of the sun's rays by the rain.",
    "There is, according to legend, a boiling pot of gold at one end."
]

# Fetch available voices
try:
    voices = polly.describe_voices()
except boto3.exceptions.Boto3Error as e:
    print(f"Failed to fetch voices: {e}")
    exit()

# Filter for English-speaking voices
english_voices = [voice for voice in voices['Voices'] if 'English' in voice['LanguageName']]

# Create output directory for Neural engine
output_dir_neural = 'polly_audio_neural'
os.makedirs(output_dir_neural, exist_ok=True)

# Generate audio for each sentence using Neural engine
def generate_audio_neural(sentence, voice_id):
    response = polly.synthesize_speech(
        Text=sentence,
        OutputFormat='mp3',
        VoiceId=voice_id,
        Engine='neural'
    )
    return response['AudioStream'].read()

for voice in english_voices:
    for i, sentence in enumerate(sentences, start=1):
        file_name_neural = f"{output_dir_neural}/voice_{voice['Id']}_{i}.mp3"
        if not os.path.exists(file_name_neural):
            try:
                audio_stream = generate_audio_neural(sentence, voice['Id'])
                with open(file_name_neural, 'wb') as file:
                    file.write(audio_stream)
                print(f"Generated audio for sentence {i} with voice {voice['Id']} using Neural engine: {file_name_neural}")
            except polly.exceptions.EngineNotSupportedException:
                print(f"Voice {voice['Id']} does not support Neural engine. Skipping.")
            except Exception as e:
                print(f"Error generating audio for sentence {i} with voice {voice['Id']} using Neural engine: {e}")
        else:
            print(f"File {file_name_neural} already exists. Skipping generation.")

print("Neural engine audio generation complete.")
