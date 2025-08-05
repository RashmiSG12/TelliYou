from Backend.transcript import extract_video_id, fetch_transcript
from Backend.qa_chain import load_llm, create_qa_chain
from Backend.vectorStore import create_vectorstore, split_transcript
import shutil
from Backend.utils.cache import is_new_video

import ast


def main(youtube_url: str, query: str) -> str:
    video_id = extract_video_id(youtube_url)
    print(f"Extracted video ID: {video_id}")
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    transcript = fetch_transcript(video_id)
    if transcript is None:
        return "Transcript not available for this video."

    # Clean up if new video
    if is_new_video(video_id):
        shutil.rmtree(f"chroma_db/{video_id}", ignore_errors=True)
    chunks = split_transcript(transcript)
    vectorstore = create_vectorstore(chunks, video_id)
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = load_llm()
    qa_chain = create_qa_chain(llm, retriever)

    # try:
    #     response = qa_chain.invoke({"query": query})
    #     return response.get("result", "No answer found.") if response else "No response generated."
    # except Exception as e:
    #     print("Error during QA chain invoke:", e)
    #     return "An error occurred while generating the answer."
    try:
        response = qa_chain.invoke({"query": query})

        if isinstance(response, dict):
            return response.get("result", "No answer found.")
        elif isinstance(response, str):
            try:
                parsed_response = ast.literal_eval(response)
                return parsed_response.get("result", "No answer found.") if isinstance(parsed_response, dict) else response
            except:
                return response
        else:
            return str(response)
    except Exception as e:
        print("Error during QA chain invoke:", e)
        return "An error occurred while generating the answer."



# Optional
if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    query = "what is the weather report today?"
    print(main(youtube_url, query))
