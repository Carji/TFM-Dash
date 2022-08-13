import streamlit as st
import numpy as np 
import pandas as pd
from PIL import Image 
import requests
from sklearn.neighbors import NearestNeighbors
def app():



        st.markdown("""---""") 
        st.header("Recomendación de títulos empleando K-Nearest Neighbors")
        st.markdown("""---""")


         

        with st.sidebar:   
            cs = st.columns(1)
            with cs[0]:
                st.subheader("Parámetros para el recomendador")
                knn_n=st.slider("Valor del parámetro K:", min_value=1, max_value=1000, value=350)
                metric_var=st.selectbox("Métrica a emplear:", options=('euclidean', 'manhattan', 'minkowski', 'chebyshev'))
                leaf_var=st.slider("Mínimo de puntos por nodo:", min_value=1, max_value=300, value=30)
                reco=st.slider('Indica cuántas recomendaciones quieres obtener', min_value=1, max_value=10, value=3)



                st.write('Por defecto se consideran los géneros y score normalizado del título seleccionado para realizar la recomendación.')

                if st.checkbox("Incluir el año de lanzamiento del título como criterio:"):
                    criterio_anyo=1
                else: 
                    criterio_anyo=0

        column_0 = 16
        column_x=193+criterio_anyo

        neigh = NearestNeighbors(n_neighbors=knn_n, leaf_size=leaf_var, metric=metric_var)

        def load_data():
            data = pd.read_csv("games-data-cleaned.csv")
            return data

        df_etl = load_data()
        neigh.fit(df_etl.iloc[:,column_0:column_x])

        st.subheader("Título sobre el que se realiza la recomendación")
        cs2 = st.columns(1)
        with cs2[0]:
             game =st.selectbox('Selecciona un título (admite entrada por texto)', df_etl.sort_values(by='score', ascending=False).name.unique())

             platf =st.selectbox('Selecciona la plataforma del título indicado (admite entrada por texto)', df_etl[df_etl['name']==game].sort_values(by='score', ascending=False).platform.unique())
             df_pick=df_etl[df_etl['name']==game]
             df_pick_plat=df_pick[df_pick['platform']==platf]
             st.write(df_pick_plat)
        input_game = np.array(df_pick_plat)[:,column_0:column_x]

        if len(input_game)!=0:
            index_closest = list(neigh.kneighbors(input_game)[1][0,0:])
        else:
            index_closest = { 0 : "3",1: "12", 2: "22", 3: "33", 4: "65"}

        df_closest=df_etl[df_etl.index.isin(index_closest)]

        df=df_closest[df_closest['name']!=game]
        df=df[df.index.isin(index_closest)]

        st.markdown("""---""")

        st.subheader("Juegos recomendados, ordenados por 'cercanía' y score")
        st.write(" ")

        recom=df.sort_values(ascending=False, by='score').reset_index(drop=True)

        for i in range(reco):

            st.markdown("""---""")
            col1, mid, col2, mid, col3 = st.columns([2,5,8,1,12])
            with col1:
                    st.image(Image.open(requests.get(recom.loc[i, 'images'], stream=True).raw), width=200)
            with col2:
                    st.write("Nombre: ",recom.loc[i, 'name'])
                    st.write("Plataforma: ", recom.loc[i, 'platform'])
                    st.write("Metascore: ",recom.loc[i, 'score'] )
                    st.write("User Score: ",recom.loc[i, 'user_score'] )
                    if recom.loc[i, 'critics']<1:
                        st.write("Sin críticas.")
                    else:
                        st.write("Críticas Positivas: ",str(round(int(recom.loc[i, 'critics_positive'])/int(recom.loc[i, 'critics'])*100,2)),'%')
                    st.write(recom.loc[i, 'r-date'])
            with col3:
                    st.write("Desarrollador: ",recom.loc[i, 'developer'])
                    st.write("Generos: ",recom.loc[i, 'genre'])
                    st.write("Resumen: ",recom.loc[i, 'summary'])


        if st.checkbox("Marcar para mostrar el dataframe de los juegos recomendados:"):
            st.write(df[:24].iloc[:,0:15])
                            

    