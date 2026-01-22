
import requests
import streamlit as st
from typing import Optional, Dict
import time



# =============================
# CONFIG
# =============================
API_BASE = "https://movie-rec-466x.onrender.com" or "http://127.0.0.1:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# =============================
# LOADING SCREEN
# =============================
if "app_loaded" not in st.session_state:
    st.session_state.app_loaded = False

if not st.session_state.app_loaded:
    # Create centered loading screen
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("")
        st.write("")
        st.write("")
        
        # Movie emoji header
        st.markdown("# 🎬")
        st.title("Movie Recommender")
        st.caption("Discover your next favorite movie")
        
        st.write("")
        
        # Progress bar with stages
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        loading_stages = [
            ("🎭 Initializing movie database...", 15),
            ("🎥 Loading recommendations engine...", 35),
            ("🍿 Preparing your experience...", 55),
            ("⭐ Fetching trending movies...", 75),
            ("🎬 Almost ready...", 90),
            ("✨ Welcome!", 100),
        ]
        
        for stage_text, progress in loading_stages:
            status_text.text(stage_text)
            progress_bar.progress(progress)
            time.sleep(0.4)
        
        time.sleep(0.3)
        
        # Clear loading elements
        progress_bar.empty()
        status_text.empty()
        
        # Show success message with movie theme
        st.success("🎬 Lights, Camera, Action! Your movie experience is ready!")
        
        # Display a row of movie emojis as visual celebration
        emoji_cols = st.columns(7)
        movie_emojis = ["🎬", "🍿", "🎥", "⭐", "🎭", "🎞️", "🏆"]
        for i, col in enumerate(emoji_cols):
            with col:
                st.markdown(f"<h1 style='text-align: center;'>{movie_emojis[i]}</h1>", unsafe_allow_html=True)
        
        time.sleep(1.2)
        
        # Toast notification
        st.toast("🍿 Welcome to Movie Recommender!", icon="🎬")
        
        # Mark as loaded
        st.session_state.app_loaded = True
        time.sleep(0.5)
        st.rerun()

# =============================
# STYLES (enhanced modern)
# =============================
st.markdown(
    """
<style>
/* Global Layout */
.block-container { 
    padding-top: 1rem; 
    padding-bottom: 2rem; 
    max-width: 1400px; 
}

/* Typography */
.small-muted { 
    color: #6b7280; 
    font-size: 0.92rem; 
}

.movie-title { 
    font-size: 0.95rem; 
    font-weight: 600;
    line-height: 1.3rem; 
    height: 2.6rem; 
    overflow: hidden;
    text-align: center;
    margin-top: 10px;
    color: #1f2937;
}

/* Cards */
.card { 
    border: none;
    border-radius: 20px; 
    padding: 24px; 
    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

/* Movie Poster Container */
.poster-container {
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    transition: all 0.3s ease;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.poster-container:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.poster-container img {
    width: 100%;
    display: block;
    transition: transform 0.3s ease;
}

.poster-container:hover img {
    transform: scale(1.05);
}

/* Rating Badge */
.rating-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 700;
    color: white;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
}

.rating-high { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
.rating-medium { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }
.rating-low { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); }

/* Section Headers */
.section-header {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 12px;
}

.section-header-icon {
    font-size: 1.8rem;
}

/* Hero Section */
.hero-container {
    text-align: center;
    padding: 2rem 0 1.5rem 0;
}

.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
}

.hero-subtitle {
    font-size: 1.1rem;
    color: #6b7280;
    font-weight: 500;
}

/* Search Box Enhancement */
.stTextInput > div > div > input {
    border-radius: 16px !important;
    border: 2px solid #e5e7eb !important;
    padding: 16px 20px !important;
    font-size: 1.05rem !important;
    transition: all 0.3s ease !important;
    outline: none !important;
}

.stTextInput > div > div > input:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15) !important;
    outline: none !important;
}

/* Remove default Streamlit input container border */
.stTextInput > div {
    border: none !important;
}

.stTextInput > div > div {
    border: none !important;
}

/* Button Styling */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    border: none !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15) !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
}

/* Selectbox Styling */
.stSelectbox > div > div {
    border-radius: 12px !important;
}

/* Metric Display */
.metric-container {
    text-align: center;
    padding: 16px;
    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 16px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.metric-label {
    font-size: 0.9rem;
    color: #6b7280;
    font-weight: 500;
}

/* Divider */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #e5e7eb, transparent);
    margin: 2rem 0;
}

/* Sidebar Styling */
.css-1d391kg, [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
}

/* No Poster Placeholder - matches movie poster 2:3 aspect ratio */
.no-poster {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 16px;
    text-align: center;
    color: white;
    font-size: 3rem;
    aspect-ratio: 2 / 3;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# STATE + ROUTING (single-file pages)
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"  # home | details
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)  # short cache for autocomplete
def api_get_json(path: str, params: Optional[Dict] = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
                <div style='text-align: center; padding: 3rem;'>
                    <div style='font-size: 4rem; margin-bottom: 1rem;'>🎬</div>
                    <div style='font-size: 1.2rem; font-weight: 600; color: #374151;'>No movies found</div>
                    <div style='color: #6b7280; margin-top: 0.5rem;'>Try a different search or category</div>
                </div>
            """, unsafe_allow_html=True)
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols)
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")
            rating = m.get("vote_average", 0)

            with colset[c]:
                # Poster with enhanced container - using aspect-ratio for consistency
                if poster:
                    st.markdown(f"""
                        <div class='poster-container' style='aspect-ratio: 2/3; overflow: hidden;'>
                            <img src='{poster}' alt='{title}' style='width: 100%; height: 100%; object-fit: cover;'>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div class='no-poster'>
                            <span>🎬</span>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Movie title
                st.markdown(f"<div class='movie-title'>{title}</div>", unsafe_allow_html=True)
                
                # Rating badge - always show something for consistent height
                if rating and rating > 0:
                    rating_class = "rating-high" if rating >= 7 else "rating-medium" if rating >= 5 else "rating-low"
                    st.markdown(f"""
                        <div style='text-align: center; margin: 8px 0; height: 36px; display: flex; align-items: center; justify-content: center;'>
                            <span class='rating-badge {rating_class}'>⭐ {rating:.1f}</span>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    # Placeholder to maintain consistent card height
                    st.markdown("""
                        <div style='text-align: center; margin: 8px 0; height: 36px; display: flex; align-items: center; justify-content: center;'>
                            <span style='color: #9ca3af; font-size: 0.85rem;'>No rating</span>
                        </div>
                    """, unsafe_allow_html=True)
                
                # View button
                if st.button("🎬 View", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}", use_container_width=True, type="primary"):
                    if tmdb_id:
                        goto_details(tmdb_id)


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                }
            )
    return cards


# =============================
# IMPORTANT: Robust TMDB search parsing
# Supports BOTH API shapes:
# 1) raw TMDB: {"results":[{id,title,poster_path,...}]}
# 2) list cards: [{tmdb_id,title,poster_url,...}]
# =============================
def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    """
    Returns:
      suggestions: list[(label, tmdb_id)]
      cards: list[{tmdb_id,title,poster_url}]
    """
    keyword_l = keyword.strip().lower()

    # A) If API returns dict with 'results'
    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                }
            )

    # B) If API returns already as list
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            # might be {tmdb_id,title,poster_url}
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": poster_url,
                    "release_date": m.get("release_date", ""),
                }
            )
    else:
        return [], []

    # Word-match filtering (contains)
    matched = [x for x in raw_items if keyword_l in x["title"].lower()]

    # If nothing matched, fallback to raw list (so never blank)
    final_list = matched if matched else raw_items

    # Suggestions = top 10 labels
    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    # Cards = top N
    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards


# =============================
# SIDEBAR (enhanced)
# =============================
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <div style='font-size: 2.5rem;'>🎬</div>
            <div style='font-size: 1.3rem; font-weight: 700; margin-top: 0.5rem;'>Movie Hub</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🏠 Home", use_container_width=True, type="primary"):
        goto_home()
    
    st.markdown("")
    st.markdown("#### 📺 Browse Categories")
    
    category_options = {
        "trending": "🔥 Trending Now",
        "popular": "⭐ Most Popular",
        "top_rated": "🏆 Top Rated",
        "now_playing": "🎬 Now Playing",
        "upcoming": "🎯 Coming Soon"
    }
    
    home_category = st.selectbox(
        "Select Category",
        list(category_options.keys()),
        format_func=lambda x: category_options[x],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("")
    st.markdown("#### ⚙️ Display Settings")
    grid_cols = st.slider("Grid Columns", 4, 8, 6, help="Adjust number of movies per row")
    
    st.markdown("---")
    
    # Tips section
    st.markdown("""
        <div style='background: linear-gradient(145deg, #f0f9ff 0%, #e0f2fe 100%); 
                    padding: 16px; border-radius: 12px; margin-top: 1rem;'>
            <div style='font-weight: 600; margin-bottom: 8px;'>💡 Quick Tips</div>
            <div style='font-size: 0.85rem; color: #4b5563; line-height: 1.5;'>
                • Search for any movie title<br>
                • Click a poster for details<br>
                • Get personalized recommendations
            </div>
        </div>
    """, unsafe_allow_html=True)

# =============================
# HEADER (Hero Section)
# =============================
st.markdown("""
    <div class='hero-container'>
        <div class='hero-title'>🎬 Movie Recommender</div>
        <div class='hero-subtitle'>Discover amazing movies and get personalized recommendations</div>
    </div>
""", unsafe_allow_html=True)

st.divider()

# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":
    # Search section with better styling
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        typed = st.text_input(
            "🔍 Search Movies",
            placeholder="Search for any movie... (e.g., Avengers, Inception, Titanic)",
            label_visibility="collapsed"
        )

    st.divider()

    # SEARCH MODE (Autocomplete + word-match results)
    if typed.strip():
        if len(typed.strip()) < 2:
            st.info("💡 Type at least 2 characters to start searching...")
        else:
            with st.spinner("🔍 Searching movies..."):
                data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"❌ Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(
                    data, typed.strip(), limit=24
                )

                # Quick select dropdown
                if suggestions:
                    st.markdown("#### 🎯 Quick Select")
                    labels = ["-- Choose a movie to view details --"] + [s[0] for s in suggestions]
                    selected = st.selectbox(
                        "Quick Select", 
                        labels, 
                        index=0,
                        label_visibility="collapsed"
                    )

                    if selected != "-- Choose a movie to view details --":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.warning("🔍 No exact matches found. Showing related results...")

                st.markdown("")
                st.markdown(f"""
                    <div class='section-header'>
                        <span class='section-header-icon'>🎬</span>
                        <span>Search Results for "{typed.strip()}"</span>
                    </div>
                """, unsafe_allow_html=True)
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")

        st.stop()

    # HOME FEED MODE
    category_icons = {
        "trending": "🔥",
        "popular": "⭐",
        "top_rated": "🏆",
        "now_playing": "🎬",
        "upcoming": "🎯"
    }
    
    category_descriptions = {
        "trending": "What everyone's watching right now",
        "popular": "Fan favorites loved by millions",
        "top_rated": "Critically acclaimed masterpieces",
        "now_playing": "Currently in theaters",
        "upcoming": "Coming to theaters soon"
    }
    
    icon = category_icons.get(home_category, "🎬")
    desc = category_descriptions.get(home_category, "")
    
    st.markdown(f"""
        <div class='section-header'>
            <span class='section-header-icon'>{icon}</span>
            <span>{home_category.replace('_',' ').title()}</span>
        </div>
        <div style='color: #6b7280; margin-top: -1rem; margin-bottom: 1.5rem;'>{desc}</div>
    """, unsafe_allow_html=True)

    with st.spinner(f"{icon} Loading {home_category.replace('_', ' ')} movies..."):
        home_cards, err = api_get_json(
            "/home", params={"category": home_category, "limit": 24}
        )
    
    if err or not home_cards:
        st.error(f"❌ Failed to load movies: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")

# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("⚠️ No movie selected.")
        if st.button("🏠 Back to Home", type="primary"):
            goto_home()
        st.stop()

    # Top navigation bar
    nav_left, nav_right = st.columns([4, 1])
    with nav_right:
        if st.button("← Back to Home", use_container_width=True):
            goto_home()

    # Load movie details
    with st.spinner("🎬 Loading movie details..."):
        data, err = api_get_json(f"/movie/id/{tmdb_id}")
    
    if err or not data:
        st.error(f"❌ Could not load details: {err or 'Unknown error'}")
        st.stop()

    # Movie title header
    st.markdown(f"""
        <div class='hero-container' style='padding: 1rem 0;'>
            <div class='hero-title' style='font-size: 2.2rem;'>{data.get('title', 'Unknown Movie')}</div>
        </div>
    """, unsafe_allow_html=True)

    # Layout: Poster LEFT, Details RIGHT
    left, right = st.columns([1, 2.5], gap="large")

    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if data.get("poster_url"):
            st.markdown(f"""
                <div class='poster-container'>
                    <img src='{data['poster_url']}' alt='Movie Poster'>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div class='no-poster'>🎬</div>", unsafe_allow_html=True)
        
        # Rating display
        rating = data.get("vote_average", 0)
        vote_count = data.get("vote_count", 0)
        if rating:
            rating_class = "rating-high" if rating >= 7 else "rating-medium" if rating >= 5 else "rating-low"
            st.markdown(f"""
                <div style='text-align: center; margin-top: 1rem;'>
                    <span class='rating-badge {rating_class}' style='font-size: 1.1rem; padding: 10px 20px;'>
                        ⭐ {rating:.1f} / 10
                    </span>
                    <div style='color: #6b7280; font-size: 0.85rem; margin-top: 8px;'>
                        {vote_count:,} votes
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        # Movie metadata
        release = data.get("release_date") or "Unknown"
        genres = ", ".join([g["name"] for g in data.get("genres", [])]) or "Unknown"
        runtime = data.get("runtime", 0)
        
        # Info grid
        info_cols = st.columns(3)
        with info_cols[0]:
            st.markdown("""
                <div class='metric-container'>
                    <div style='font-size: 1.5rem;'>📅</div>
                    <div class='metric-label'>Release Date</div>
                    <div style='font-weight: 600; color: #374151;'>""" + release + """</div>
                </div>
            """, unsafe_allow_html=True)
        
        with info_cols[1]:
            st.markdown("""
                <div class='metric-container'>
                    <div style='font-size: 1.5rem;'>🎭</div>
                    <div class='metric-label'>Genres</div>
                    <div style='font-weight: 600; color: #374151; font-size: 0.85rem;'>""" + genres + """</div>
                </div>
            """, unsafe_allow_html=True)
        
        with info_cols[2]:
            runtime_str = f"{runtime} min" if runtime else "N/A"
            st.markdown("""
                <div class='metric-container'>
                    <div style='font-size: 1.5rem;'>⏱️</div>
                    <div class='metric-label'>Runtime</div>
                    <div style='font-weight: 600; color: #374151;'>""" + runtime_str + """</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("")
        st.markdown("#### 📖 Overview")
        overview = data.get("overview") or "No overview available for this movie."
        st.markdown(f"""
            <div style='background: #f8fafc; padding: 16px; border-radius: 12px; 
                        line-height: 1.7; color: #374151; font-size: 1rem;'>
                {overview}
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    # Backdrop section
    if data.get("backdrop_url"):
        st.markdown("")
        st.markdown("""
            <div class='section-header'>
                <span class='section-header-icon'>🖼️</span>
                <span>Movie Backdrop</span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <div style='border-radius: 16px; overflow: hidden; box-shadow: 0 8px 30px rgba(0,0,0,0.15);'>
                <img src='{data["backdrop_url"]}' style='width: 100%; display: block;'>
            </div>
        """, unsafe_allow_html=True)

    st.divider()
    
    # Recommendations section
    st.markdown("""
        <div class='section-header'>
            <span class='section-header-icon'>✨</span>
            <span>Recommended For You</span>
        </div>
    """, unsafe_allow_html=True)

    title = (data.get("title") or "").strip()
    if title:
        with st.spinner("🎯 Finding perfect recommendations..."):
            bundle, err2 = api_get_json(
                "/movie/search",
                params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
            )

        if not err2 and bundle:
            st.markdown("""
                <div class='section-header' style='font-size: 1.2rem; margin-top: 1rem;'>
                    <span> Similar Movies</span>
                </div>
                <div style='color: #6b7280; margin-top: -1rem; margin-bottom: 1rem; font-size: 0.9rem;'>
                    Based on storyline and themes
                </div>
            """, unsafe_allow_html=True)
            poster_grid(
                to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
                cols=grid_cols,
                key_prefix="details_tfidf",
            )

            st.markdown("")
            st.markdown("""
                <div class='section-header' style='font-size: 1.2rem; margin-top: 2rem;'>
                    <span>🎭 More Like This</span>
                </div>
                <div style='color: #6b7280; margin-top: -1rem; margin-bottom: 1rem; font-size: 0.9rem;'>
                    Similar genres you might enjoy
                </div>
            """, unsafe_allow_html=True)
            poster_grid(
                bundle.get("genre_recommendations", []),
                cols=grid_cols,
                key_prefix="details_genre",
            )
        else:
            st.info("💡 Showing genre-based recommendations...")
            with st.spinner("Loading recommendations..."):
                genre_only, err3 = api_get_json(
                    "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
                )
            if not err3 and genre_only:
                poster_grid(
                    genre_only, cols=grid_cols, key_prefix="details_genre_fallback"
                )
            else:
                st.warning("😔 No recommendations available at the moment. Please try again later.")
    else:
        st.warning("⚠️ Unable to compute recommendations for this movie.")