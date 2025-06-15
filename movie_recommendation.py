import streamlit as st
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from duckduckgo_search import DDGS
import wikipedia
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_base = os.getenv("AZURE_OPENAI_API_BASE")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Page setup
st.set_page_config(page_title="CineMatch AI", layout="wide", page_icon="🎬")
st.title("🎬 CineMatch AI - Get your Bollywood Movie Recommendations")

# Sidebar for preferences
with st.sidebar:
    st.header("🎯 Movie Preferences")
    genre = st.selectbox("Genre", ["Action", "Comedy", "Drama", "Romance", "Thriller", "Horror", "Sci-Fi", "Fantasy", "Musical", "Documentary", "Suspense", "Adventure", "Historical", "Mystery", "Animation", "Family", "Crime", "Biography", "Sports", "War"])
    actor = st.text_input("Actor Name")
    actress = st.text_input("Actress Name")
    director = st.text_input("Director Name")
    year_range = st.slider("Year Range", 1960, 2025, (2000, 2024))
    get_recommend = st.button("🎥 Recommend Movies")

# LLM setup
@st.cache_resource
def init_chain():
    llm = AzureChatOpenAI(
        openai_api_base=api_base,
        openai_api_version=api_version,
        openai_api_key=api_key,
        deployment_name=deployment_name,
        model_name="gpt-4o",
        temperature=0.8,
        max_tokens=500,
        top_p=0.9,
    )
    prompt = PromptTemplate(
        input_variables=["genre", "actor", "actress", "director", "start_year", "end_year"],
        template="""
Recommend 5 top Bollywood movies based on:
- Genre: {genre}
- Favorite Actor: {actor}
- Favorite Actress: {actress}
- Director: {director}
- Release Year: Between {start_year} and {end_year}

Give a brief reason for each recommendation.
"""
    )
    return LLMChain(llm=llm, prompt=prompt)

llmchain = init_chain()

# 🎬 Recommendations
if get_recommend:
    with st.spinner("Generating recommendations..."):
        response = llmchain.invoke({
            "genre": genre,
            "actor": actor,
            "actress": actress,
            "director": director,
            "start_year": year_range[0],
            "end_year": year_range[1]
        })
        st.subheader("🎬 Recommended Movies:")
        st.markdown(response['text'])

# 🔍 Search section
st.markdown("---")
st.subheader("🔎 Search Bollywood Movie Info (Wikipedia + DuckDuckGo)")

search_query = st.text_input("Enter a movie name to search")

if st.button("Search Now"):
    if not search_query.strip():
        st.warning("Please enter a movie name.")
    else:
        wiki_summary, wiki_url, ddg_results, poster_url = None, None, [], None

        # Wikipedia lookup
        try:
            wiki_summary = wikipedia.summary(search_query, sentences=5, auto_suggest=True, redirect=True)
            wiki_url = wikipedia.page(search_query, auto_suggest=True).url
        except wikipedia.DisambiguationError as e:
            wiki_summary = f"Disambiguation: try being more specific. Suggestions: {', '.join(e.options[:3])}"
        except:
            wiki_summary = None

        # DuckDuckGo search & image fetch
        try:
            with DDGS() as ddgs:
                ddg_results = list(ddgs.text(search_query + " bollywood movie", max_results=5))
                ddg_images = list(ddgs.images(search_query + " bollywood movie poster", max_results=1))
                if ddg_images:
                    poster_url = ddg_images[0]["image"]
        except:
            pass

        # Display results
        if wiki_summary or ddg_results:
            if poster_url:
                st.image(poster_url, caption="🎬 Movie Poster", use_column_width=True)

            if wiki_summary:
                st.info("📚 Wikipedia Summary")
                if wiki_url:
                    st.markdown(f"**[{search_query} on Wikipedia]({wiki_url})**")
                st.write(wiki_summary)

            if ddg_results:
                st.info("🌐 DuckDuckGo Web Results")
                for r in ddg_results:
                    st.markdown(f"**[{r['title']}]({r['href']})**")
                    st.caption(r['body'])

        else:
            st.error("❌ No results found from Wikipedia or DuckDuckGo.")
