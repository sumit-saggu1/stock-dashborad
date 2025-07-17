import streamlit as st

st.set_page_config(
    page_title="Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)

with st.container():
    col1, col2 = st.columns([1, 8])
    with col1:
        st.image("logo.png", width=70,)
    with col2:
        st.markdown("<h1 style='margin-bottom:0;'>Stock Analysis Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("""
        <span style='font-size:1.2em;color:gray;'>Analyze stocks with interactive charts and statistics.</span>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
Welcome!  
Use the sidebar to navigate between pages for different analysis views.
""")