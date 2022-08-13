import pandas as pd
import streamlit as st
from PIL import Image 
import requests



def app():
        def load_data():
            data = pd.read_csv("games-data-cleaned.csv")
            return data

        games = load_data()

        features = ["name","genre","developer","platform", "score"]
        for i in features:
            games[i] = games[i].fillna(" ")
        st.markdown("""---""") 
        st.header('Búsqueda de títulos por plataforma')
        st.markdown("""---""") 
        platform_name = st.selectbox('Select a Platform', options=games.platform.unique())
        platform_subset = st.multiselect('Selecciona un juego (admite entrada por texto)', games[games["platform"]==platform_name].sort_values(ascending=False, by='score').name.unique(), default=games[games["platform"]==platform_name].iloc[:1].name)
        st.write(" ")
        st.write(" ")
        st.write(" ")

        platform_df = games[games["platform"]==platform_name]
        plat_write_df=platform_df[platform_df["name"].isin(platform_subset)]
        st.write(plat_write_df.iloc[:,0:15])

        for i in plat_write_df.index.values:

            st.markdown("""---""")
            col1, mid, col2, mid, col3 = st.columns([2,5,8,1,12])
            with col1:
                    st.image(Image.open(requests.get(plat_write_df.loc[i, 'images'], stream=True).raw), width=200)
            with col2:
                    st.write("Nombre: ",plat_write_df.loc[i, 'name'])
                    st.write("Plataforma: ", plat_write_df.loc[i, 'platform'])
                    st.write("Metascore: ",plat_write_df.loc[i, 'score'] )
                    st.write("User Score: ",plat_write_df.loc[i, 'user_score'] )
                    if plat_write_df.loc[i, 'critics']<1:
                        st.write("Sin críticas.")
                    else:
                        st.write("Críticas Positivas: ",str(round(int(plat_write_df.loc[i, 'critics_positive'])/int(plat_write_df.loc[i, 'critics'])*100,2)),'%')
                    st.write(plat_write_df.loc[i, 'r-date'])
            with col3:
                    st.write("Desarrollador: ",plat_write_df.loc[i, 'developer'])
                    st.write("Generos: ",plat_write_df.loc[i, 'genre'])
                    st.write("Resumen: ",plat_write_df.loc[i, 'summary'])
