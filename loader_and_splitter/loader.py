from youtube_transcript_api import YouTubeTranscriptApi,TranscriptsDisabled
from langchain_text_splitters import CharacterTextSplitter
from googletrans import Translator
import asyncio

# transcript api obj
yt_api = YouTubeTranscriptApi()

translator = Translator()

# text splitter for chunking to send in the translator object
text_splitter = CharacterTextSplitter(
    separator= " ",
    chunk_size = 2000, #sending large chunk resulted in outputting untranslated transcripts
    chunk_overlap = 0
)

async def load_transcript(id):
    try:
        transcript_metadata = yt_api.list(video_id=id)

    except TranscriptsDisabled:
        print(TranscriptsDisabled)
        return None
    
    except Exception as e:
        print("Exception occured",e)
        return None
    
    if transcript_metadata:
        # getting base language
        try:
            base_languages = [x.language_code for x in transcript_metadata if not x.is_generated] #looking for manual transcritps

            if not base_languages:
                base_languages = [x.language_code for x in transcript_metadata if x.is_generated] #settling for yt generated transcripts

            if not base_languages:
                print("No transcripts available.")
                return None
            
            source_lang = base_languages[0]
            print(source_lang)
        
        except Exception as e:
            print("Exception:",e)
        
        transcript_txt = None
        if source_lang == 'en':
            fetched_txt = yt_api.fetch(video_id=id,languages=[source_lang])
            transcript_txt = " ".join(t.text for t in fetched_txt)
        else:
            transcript_txt = await translate_to_english(id,source_lang)
               


    return {'meta':transcript_metadata,'txt': transcript_txt}


async def translate_to_english(id,source_lang):
    transcript = yt_api.fetch(video_id=id,languages=[source_lang])
    full_text = " ".join(t.text for t in transcript)

    text_chunks = text_splitter.split_text(full_text)
    translated_chunks = []
    for chunk in text_chunks:
        tranlsated_text = await translator.translate(chunk,src=source_lang,dest='en')
        translated_chunks.append(tranlsated_text.text)
    
    txt = " ".join(translated_chunks)
    return txt

# output = asyncio.run(load_transcript(""))
# print(output['txt'])