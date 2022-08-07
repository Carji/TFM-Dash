import app0
import app1
import app2
import app3
import app4
import streamlit as st
st.set_page_config(layout="wide")
hojas = {
    "Análisis Exploratorio": app0,
    "Panda's Profiling Report": app2,
    "Sistema de recomendación": app1,
    "Buscador de títulos por plataforma":app4,
    "Sandbox": app3
}
st.markdown("""
    <style type="text/css">
    div[data-testid="stHorizontalBlock"] {
        border:10px;
        padding:30px;
        border-radius: 15px;
        background:#FFFFFF;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title('Contenido del Dashboard')
selection = st.sidebar.radio("", list(hojas.keys()))
page = hojas[selection]
page.app()

st.markdown("""   """)
st.markdown("""---""")
st.markdown("""   """)
st.write("### Link to Github repo:")
st.markdown("[GitHub Repository](https://github.com/carji/TFM-dash)")
