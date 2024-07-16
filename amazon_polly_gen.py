import boto3
import os

#Amazon polly credentials
polly = boto3.Session(
    aws_access_key_id='abc',
    aws_secret_access_key='xyz',
    region_name='us-east-1'
).client('polly')

#Define the senetence set
sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "She sells seashells by the seashore.",
    "How much wood would a woodchuck chuck if a woodchuck could chuck wood?",
    "Peter Piper picked a peck of pickled peppers.",
    "A big black bug bit a big black bear.",
    "I scream, you scream, we all scream for ice cream.",
    "Red leather, yellow leather.",
    "Unique New York.",
    "The cat sat on the mat.",
    "He asked for a glass of water in the middle of the night."
]

# Fetch available voices
try:
    voices = polly.describe_voices()
except boto3.exceptions.Boto3Error as e:
    print(f"Failed to fetch voices: {e}")
    exit()

# Save the audio, specify the output directory
output_dir = 'polly_audio'
os.makedirs(output_dir, exist_ok=True)

# Genrate audio for each sentence
character_count = 0
batch_limit = 100000
batch_number = 1

def generate_audio(sentence, voice_id, engine='standard'):
    try:
        response = polly.synthesize_speech(
            Text=sentence,
            OutputFormat='mp3',
            VoiceId=voice_id,
            Engine=engine
        )
        return response['AudioStream'].read()
    except polly.exceptions.ValidationException as e:
        if engine == 'standard':
            print(f"Voice {voice_id} does not support 'standard' engine, trying 'neural'.")
            return generate_audio(sentence, voice_id, engine='neural')
        else:
            raise e

for voice in voices['Voices']:
    for i, sentence in enumerate(sentences, start=1):
        if character_count + len(sentence) > batch_limit:
            batch_number += 1
            character_count = 0

        file_name = f"{output_dir}/batch_{batch_number}_voice_{voice['Id']}_{i}.mp3"
        if not os.path.exists(file_name):
            try:
                audio_stream = generate_audio(sentence, voice['Id'])
                with open(file_name, 'wb') as file:
                    file.write(audio_stream)

                character_count += len(sentence)
                print(f"Generated audio for sentence {i} with voice {voice['Id']}: {file_name}")

            except Exception as e:
                print(f"Error generating audio for sentence {i} with voice {voice['Id']}: {e}")
        else:
            print(f"File {file_name} already exists. Skipping generation.")

print("Audio generation complete.")