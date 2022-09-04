import pandas as pd
import streamlit as st
from PIL import Image 
import requests



def app():
        def load_data():
            data = pd.read_csv("data/games-data-cleaned.csv")
            return data

        games = load_data()

        features = ["Título","Géneros","Desarrollador","Plataforma", "Puntuación"]
        for i in features:
            games[i] = games[i].fillna(" ")
        st.markdown("""---""") 
        st.header('Búsqueda de títulos por plataforma')
        st.markdown("""---""") 
        platform_name = st.selectbox('Selecciona una plataforma', options=games.Plataforma.unique())
        platform_subset = st.multiselect('Selecciona un juego (admite entrada por texto)', games[games["Plataforma"]==platform_name].sort_values(ascending=False, by='Puntuación').Título.unique(), default=games[games["Plataforma"]==platform_name].iloc[:1].Título)
        st.write(" ")
        st.write(" ")
        st.write(" ")

        platform_df = games[games["Plataforma"]==platform_name]
        plat_write_df=platform_df[platform_df["Título"].isin(platform_subset)]
        st.write(plat_write_df.iloc[:,0:15])

        for i in plat_write_df.index.values:

            st.markdown("""---""")
            col1, mid, col2, mid, col3 = st.columns([2,5,8,1,12])
            with col1:
                    st.image(Image.open(requests.get(plat_write_df.loc[i, 'images'], stream=True).raw), width=200)
            with col2:
                    st.write("Título: ",plat_write_df.loc[i, 'Título'])
                    st.write("Plataforma: ", plat_write_df.loc[i, 'Plataforma'])
                    st.write("Puntuación de críticos: ",plat_write_df.loc[i, 'Puntuación'] )
                    st.write("Puntuación de usuarios: ",plat_write_df.loc[i, 'Puntuación de usuarios'] )
                    if plat_write_df.loc[i, 'Críticas']<1:
                        st.write("Sin críticas.")
                    else:
                        st.write("Críticas favorables: ",str(round(int(plat_write_df.loc[i, 'Críticas favorables'])/int(plat_write_df.loc[i, 'Críticas'])*100,2)),'%')
                    st.write("Fecha de lanzamiento: ",plat_write_df.loc[i, 'Fecha de lanzamiento'])
            with col3:
                    st.write("Desarrollador: ",plat_write_df.loc[i, 'Desarrollador'])
                    st.write("Generos: ",plat_write_df.loc[i, 'Géneros'])
                    st.write("Resumen: ",plat_write_df.loc[i, 'Resumen'])
