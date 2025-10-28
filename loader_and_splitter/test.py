from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator
import asyncio

# ytt_api = YouTubeTranscriptApi()

# transcript_metadata= ytt_api.list("CHGmM4RfeIw")

# base_languages = [x.language_code for x in transcript_metadata if not x.is_generated] #looking for manual transcritps

# if not base_languages:
#     base_languages = [x.language_code for x in transcript_metadata if x.is_generated] #settling for yt generated transcripts

# if not base_languages:
#     print("No transcripts available.")
#     base_languages = None

# source_lang = base_languages[0]
# print(source_lang)
# print(base_languages)

# fetch_out = ytt_api.fetch("CHGmM4RfeIw", languages=[source_lang])
# print(fetch_out[0])

async def main():
    from googletrans import Translator
    translator = Translator()

    # 1. Instantiate the main class
    ytt_api = YouTubeTranscriptApi()

    # 2. Fetch the Hindi transcript
    output = ytt_api.fetch("CHGmM4RfeIw", languages=['es'])
    
    # 3. Select the first segment object
    first_segment = output[0]
    
    print(first_segment.text)
    
    # 4. FIX: Use 'await' to execute the asynchronous translation
    translation = await translator.translate(first_segment.text, dest='en')
    
    # 5. Print the actual translated text content
    print(translation.text)

if __name__ == "__main__":
    asyncio.run(main())
