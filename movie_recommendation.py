import streamlit as st
from langchain_community.chat_models import AzureChatOpenAI
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

# Page config and theme
st.set_page_config(page_title="CineMatch AI", layout="wide", page_icon="🎞️")

st.markdown("<h1 style='text-align: center;'>🎬 CineMatch AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #34495e;'>Your personalized Bollywood movie guide for Bollywood Diwane</p>", unsafe_allow_html=True)

# Sidebar Preferences
with st.sidebar:
    st.header("🎯 Movie Preferences")
    genre = st.selectbox("Choose Genre", ["Action", "Comedy", "Drama", "Romance", "Thriller", "Horror", "Sci-Fi", "Fantasy", "Musical", "Documentary", "Suspense", "Adventure", "Historical", "Mystery", "Animation", "Family", "Crime", "Biography", "Sports", "War", "Western", "Musical", "Dance", "Mythology", "Social Issues", "Psychological", "Superhero"])
    actor = st.text_input("Favorite Actor")
    actress = st.text_input("Favorite Actress")
    director = st.text_input("Favorite Director")
    year_range = st.slider("Year Range", 1960, 2025, (2000, 2024))
    get_recommend = st.button("🎥 Recommend Movies")

# Initialize LLM
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

# Recommendation section
if get_recommend:
    with st.spinner("✨ Finding the perfect movies for you..."):
        response = llmchain.invoke({
            "genre": genre,
            "actor": actor,
            "actress": actress,
            "director": director,
            "start_year": year_range[0],
            "end_year": year_range[1]
        })
        st.subheader("🎬 Top Picks Just for You")
        st.markdown(f"<div class='big-font'>{response['text']}</div>", unsafe_allow_html=True)

# Separator
st.markdown("---")

# Movie search
st.subheader("🔍 Movie Info Lookup")
search_query = st.text_input("Enter a movie name to search", placeholder="e.g. Laila Majnu 2018")

if st.button("🔎 Search Now"):
    if not search_query.strip():
        st.warning("⚠️ Please enter a valid movie name.")
    else:
        wiki_summary, wiki_url, ddg_results, poster_url = None, None, [], None

        # Wikipedia fetch
        try:
            wiki_summary = wikipedia.summary(search_query, sentences=5, auto_suggest=True, redirect=True)
            wiki_url = wikipedia.page(search_query, auto_suggest=True).url
        except wikipedia.DisambiguationError as e:
            wiki_summary = f"Too many matches. Try one of: {', '.join(e.options[:3])}"
        except:
            wiki_summary = None

        # DuckDuckGo search and poster
        try:
            with DDGS() as ddgs:
                ddg_results = list(ddgs.text(search_query + " bollywood movie", max_results=5))
                ddg_images = list(ddgs.images(search_query + " bollywood movie poster", max_results=1))
                if ddg_images:
                    poster_url = ddg_images[0]["image"]
        except:
            pass

        if wiki_summary or ddg_results:
            st.markdown("## 🧾 Movie Overview")

            if poster_url:
                st.image(poster_url, caption="🎞️ Poster", use_column_width=True)

            col1, col2 = st.columns(2)

            if wiki_summary:
                with col1:
                    st.info("📚 Wikipedia")
                    if wiki_url:
                        st.markdown(f"🔗 [View on Wikipedia]({wiki_url})")
                    st.write(wiki_summary)

            if ddg_results:
                with col2:
                    st.info("🌐 DuckDuckGo Web Links")
                    for r in ddg_results:
                        st.markdown(f"🔗 **[{r['title']}]({r['href']})**")
                        st.caption(r['body'])
        else:
            st.error("🚫 No info found on this movie. Try a different name.")
