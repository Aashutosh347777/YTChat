from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator
import asyncio

async def main():
    from googletrans import Translator
    translator = Translator()

    # 1. Instantiate the main class
    ytt_api = YouTubeTranscriptApi()

    # 2. Fetch the Hindi transcript
    output = ytt_api.fetch("fHBR1j1kJ1I", languages=['hi'])
    
    # 3. Select the first segment object
    first_segment = output[0]
    
    print(first_segment.text)
    
    # 4. FIX: Use 'await' to execute the asynchronous translation
    translation = await translator.translate(first_segment.text, dest='en')
    
    # 5. Print the actual translated text content
    print(translation.text)

if __name__ == "__main__":
    asyncio.run(main())

# # 2. Retrieve the list of available transcripts
# transcript_list = ytt_api.list('aircAruvnKk')

# # 3. Find the original English transcript object (assuming English is the source language)
# transcript = transcript_list.find_transcript(['en'])

# # 4. Use the .translate() method to get a new, translated Transcript object
# # Note: 'de' is for German, NOT Spanish. 'es' would be for Spanish.
# translated_transcript = transcript.translate('de') 

# # 5. Fetch the data from the translated object and print
# translated_data = translated_transcript.fetch()
# print(translated_data)