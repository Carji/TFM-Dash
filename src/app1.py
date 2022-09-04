import streamlit as st
import numpy as np 
import pandas as pd
from PIL import Image 
import requests
from sklearn.neighbors import NearestNeighbors
def app():

        st.markdown("""---""") 
        st.header("Recomendación de títulos empleando el algoritmo de los vecinos más cercanos")
        st.markdown("""---""")

        métricas = {
         "Distancia euclidiana": 'euclidean',
         "Distancia Manhattan": 'manhattan',
         "Distancia Minkowski": 'minkowski',
         "Distancia Chebyshev": 'chebyshev',
         "Similaridad coseno": 'cosine'
}

        with st.sidebar:   
            cs = st.columns(1)
            with cs[0]:
                st.subheader("Hiperparámetros para el recomendador")
                knn_n=st.slider("Valor del número de vecinos más cercanos:", min_value=1, max_value=1000, value=350)
                metric_var=st.selectbox("Métrica a emplear:", options=list(métricas.keys()))
                leaf_var=st.slider("Mínimo de puntos por nodo:", min_value=1, max_value=300, value=30)
                reco=st.slider('Indica cuántas recomendaciones quieres obtener:', min_value=1, max_value=10, value=3)

                st.write('Por defecto se consideran los géneros y score normalizado del título seleccionado para realizar la recomendación.')

                if st.checkbox("Marcar la casilla para incluir el año de lanzamiento del título como variable predictora"):
                    criterio_anyo=1
                else: 
                    criterio_anyo=0

        column_0 = 16
        column_x=194+criterio_anyo

        neigh = NearestNeighbors(n_neighbors=knn_n, leaf_size=leaf_var, metric=métricas.get(metric_var), n_jobs=-1)

        def load_data():
            data = pd.read_csv("data/games-data-cleaned.csv")
            return data

        df_etl = load_data()
        neigh.fit(df_etl.iloc[:,column_0:column_x])

        st.subheader("Título sobre el que se realiza la recomendación")

        cs2 = st.columns(1)
        with cs2[0]:
             game =st.selectbox('Selecciona un título (admite entrada por texto)', df_etl.sort_values(by='Puntuación', ascending=False).Título.unique())

             platf =st.selectbox('Selecciona la plataforma del título indicado (admite entrada por texto)', df_etl[df_etl['Título']==game].sort_values(by='Puntuación', ascending=False).Plataforma.unique())
             df_pick=df_etl[df_etl['Título']==game]
             df_pick_plat=df_pick[df_pick['Plataforma']==platf]
             st.write(df_pick_plat)
        input_game = np.array(df_pick_plat)[:,column_0:column_x]

        if len(input_game)!=0:
            index_closest = list(neigh.kneighbors(input_game)[1][0,0:])
        else:
            index_closest = { 0 : "3",1: "12", 2: "22", 3: "33", 4: "65"}

        df_closest=df_etl[df_etl.index.isin(index_closest)]

        df=df_closest[df_closest['Título']!=game]
        df=df[df.index.isin(index_closest)]
        filtered_selfindex= [x for x in index_closest if x not in df_closest[df_closest['Título']==game].index.values]
        st.markdown("""---""")

        st.subheader("Juegos recomendados, ordenados por distancia al seleccionado")
        st.write(" ")

        recom=df
        slot=-1
        for i in filtered_selfindex[0:reco]:
            slot=slot+1
            st.markdown("""---""")
            col1, mid, col2, mid, col3 = st.columns([2,5,8,1,12])
            with col1:
                    st.image(Image.open(requests.get(recom.loc[i, 'images'], stream=True).raw), width=200)
            with col2:
                    st.write("Título: ",recom.loc[i, 'Título'])
                    st.write("Plataforma: ", recom.loc[i, 'Plataforma'])
                    st.write("Puntuación de críticos: ",recom.loc[i, 'Puntuación'] )
                    st.write("Puntuación de usuarios: ",recom.loc[i, 'Puntuación de usuarios'] )
                    if recom.loc[i, 'Críticas']<1:
                        st.write("Sin críticas.")
                    else:
                        st.write("Críticas favorables: ",str(round(int(recom.loc[i, 'Críticas favorables'])/int(recom.loc[i, 'Críticas'])*100,2)),'%')
                    st.write("Fecha de lanzamiento: ",recom.loc[i, 'Fecha de lanzamiento'])
            with col3:
                    st.write("Desarrollador: ",recom.loc[i, 'Desarrollador'])
                    st.write("Géneros: ",recom.loc[i, 'Géneros'])
                    st.write("Resumen: ",recom.loc[i, 'Resumen'],"...")
                    st.write("Distancia al título seleccionado: ",round(neigh.kneighbors(input_game)[0][0,slot],3))

        if st.checkbox("Marcar para mostrar el dataframe de los juegos recomendados:"):
            st.write(df[:24].iloc[:,0:15])
                            

    