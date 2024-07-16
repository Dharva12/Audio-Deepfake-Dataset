from elevenlabs.client import ElevenLabs

# Set the API key for ElevenLabs
client = ElevenLabs(api_key="sk_68b4b42e8e8da72a711bbda6ab3be505a604241d3d585901")

# Fetch available voices
voices = client.voices.get_all()
for voice in voices.voices:
    print(f"Voice Name: {voice.name}, Voice ID: {voice.voice_id}")

# Define the sentences for ElevenLabs
group_1 = [
    "I set a trap near the car to catch the mouse.",
    "After the bath, she caught a glimpse of the advertisement.",
    "The cat sat on the mat and looked at the hat.",
    "He asked for a glass of water in the middle of the night.",
    "The children laughed as they danced in the park.",
    "She wore a red dress and a black hat to the event.",
    "He parked the car near the large garage.",
    "The farmer harvested the corn and the wheat.",
    "She enjoys reading books in her free time.",
    "The teacher gave a long lecture on mathematics.",
    "He bought a new pair of shoes at the store.",
    "The dog barked loudly at the stranger.",
    "They enjoyed a delicious meal at the new restaurant.",
    "The movie was fantastic and very entertaining.",
    "He completed the marathon in record time.",
    "The flowers in the garden were blooming beautifully.",
    "She received a lot of praise for her performance.",
    "The weather was perfect for a day at the beach.",
    "He watched the football game with great interest.",
    "The new software update improved performance.",
    "She sang a song with a beautiful melody.",
    "The artist painted a stunning portrait.",
    "He fixed the broken chair with some glue.",
    "The chef prepared a gourmet meal for the guests.",
    "The cat chased the mouse around the house.",
    "She found a rare book at the antique shop.",
    "He drove carefully on the icy road.",
    "The conference was attended by many experts.",
    "She practiced the piano for several hours.",
    "He solved the complex puzzle quickly.",
    "The team worked together to achieve their goal.",
    "The bird built a nest in the tree.",
    "She baked a delicious cake for the party.",
    "He wrote a letter to his friend overseas.",
    "The engineer designed a new bridge."
]

# Fetch available voices
voices = client.voices.get_all()

for voice in voices.voices:
    for i, prompt in enumerate(group_1, start=1):
        audio_generator = client.generate(
            text=prompt,
            voice=voice.voice_id,
            model="eleven_multilingual_v2"
        )

        audio = b''.join(list(audio_generator))
        file_name = f"output_elevenlabs_{voice.name}_{i}.mp3"
        with open(file_name, "wb") as f:
            f.write(audio)
        print(f"Generated audio for prompt {i} with voice {voice.name}: {file_name}")