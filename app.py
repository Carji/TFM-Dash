from src import app0, app1, app2, app3, app4
import streamlit as st
st.set_page_config(layout="wide")
hojas = {
    "Análisis exploratorio": app0,
# App2 Desactivada en cloud, no funciona con capas gratuitas. En local funciona OK.
#    "Panda's Profiling Report": app2, 
    "Sistema de recomendación": app1,
    "Buscador de títulos por plataforma":app4,
    "Entorno de pruebas": app3
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

st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)
st.title('Cuadro de mando para análisis exploratorio y recomendación de videojuegos🕹️')
st.sidebar.image('img/cidaen.png')
st.sidebar.title('Contenido de la aplicación')

selection = st.sidebar.radio("", list(hojas.keys()))
page = hojas[selection]
page.app()

st.markdown("""   """)
st.markdown("""---""")
st.markdown("""   """)
st.write("### Link to Github repo:")
st.markdown("[GitHub Repository](https://github.com/carji/TFM-dash)")
