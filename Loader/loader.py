from youtube_transcript_api import YouTubeTranscriptApi,TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_transcript(id):
    try:
        api = YouTubeTranscriptApi()
        transcript_metadata = api.list(video_id=id)

    except TranscriptsDisabled:
        print(TranscriptsDisabled)
        return None
    
    except Exception as e:
        print("Exception occured",e)
        return None
    
    if transcript_metadata:
        # checking for available english transation
        eng_available_main = any(str(x.language_code).lower() == 'en' for x in transcript_metadata)
        eng_translatable = any(
            any(t.language_code.lower() == 'en' for t in x.translation_languages) 
            for x in transcript_metadata
        )
        eng_available = eng_available_main or eng_translatable

        # getting base language
        try:
            base_languages = [x.language_code for x in transcript_metadata if not x.is_generated] #looking for manual transcritps

            if not base_languages:
                base_languages = [x.language_code for x in transcript_metadata if x.is_generated] #settling for yt generated transcripts

            if not base_languages:
                print("No transcripts available.")
                return None
            
            source_lang = base_languages[0]
        
        except Exception as e:
            print("Exception:",e)
        
        transcript_txt = None
        if source_lang:
            if eng_available:
                print('we dint enter')
                transcript_source = api.fetch(video_id = id,languages=source_lang)
                transcript_eng = transcript_source.translate('en')
            else:
                pass
                # translate to english


    return {'meta':transcript_metadata,'txt': transcript_eng}


output = load_transcript("DtG4DGaPgcE")
print(output['meta'])

print("\n---transcript---",output['txt'])