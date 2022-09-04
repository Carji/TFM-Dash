import pandas as pd
import streamlit as st
import plotly.express as px

def app():
    st.markdown("""---""") 
    st.header("Análisis exploratorio de títulos de videojuegos")

    picker = st.sidebar.selectbox("Desplegable", ["Análisis por plataforma", "Análisis por otros ejes"], key="sidebarselector")

    if picker == "Análisis por plataforma":
        df_games = pd.read_csv("data/games-data-cleaned.csv")
        st.markdown("""---""") 
        cc = st.columns(2)

        with cc[0]:
            st.write('## Distribución de títulos por plataforma')  
            df_pie=df_games.groupby('Plataforma').count().rename(columns = {'Título':'Nº de títulos'})       
            fig = px.pie(df_pie, values='Nº de títulos', names=df_pie.index.values,
            labels=dict(label="Plataforma"))
            fig.update_traces(textposition='inside')
            fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

            st.plotly_chart(fig, use_container_width=True)

        with cc[1]:
            st.write('## Valores medios por plataforma') 
            df_table=df_games[df_games['Puntuación'] != 0.0].groupby('Plataforma').mean().iloc[:,:7]#.sort_values(by='Puntuación', ascending=False)
            st.write(df_table)
            st.write("Nota: Se excluyen los títulos no puntuados por la crítica.")

        df_evol=df_games.groupby(['Año', 'Plataforma']).count().reset_index().rename(columns = {'Título':'títulos'})

        fig = px.histogram(df_evol, x="Año",y='títulos',color='Plataforma', opacity = 0.8,
          labels={'Plataforma':'Plataforma', 'Año':'Periodo'}, nbins=35).update_layout(
            yaxis_title="Número de títulos")

        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

        cs = st.columns(1)
        with cs[0]:
            st.write('## Histograma anual de títulos por plataforma') 
            st.plotly_chart(fig, use_container_width=True)

    if picker == "Análisis por otros ejes":   
        df_games = pd.read_csv("data/games-data-cleaned.csv") 
        df_games["Fecha de lanzamiento"]=pd.to_datetime(df_games["Fecha de lanzamiento"])
        st.markdown("""---""")  

            
        with st.sidebar:            
            st.markdown("""   """)  
            st.markdown("""---""")  

            csx = st.columns(1)
            with csx[0]:
                bar_x = st.selectbox("Dimensión de tarta", ["Plataforma","Fecha de lanzamiento","Puntuación","Puntuación de usuarios","Desarrollador","Géneros","Nº de jugadores","Nº de géneros"],index=0)
                x_axis = st.selectbox("Eje X", ["Puntuación","Puntuación de usuarios","Plataforma","Fecha de lanzamiento","Géneros","Nº de géneros","Nº de jugadores","Críticas","Críticas favorables","Críticas neutrales","Críticas desfavorables","Nº valoraciones de usuario"],index=0)
                y_axis = st.selectbox("Eje Y (Nube de puntos)", ["Puntuación","Puntuación de usuarios","Plataforma","Fecha de lanzamiento","Géneros","Nº de géneros","Nº de jugadores","Críticas","Críticas favorables","Críticas neutrales","Críticas desfavorables","Nº valoraciones de usuario"],index=1)
                color_sc = st.selectbox("Paleta de colores", ['Plataforma', 'Puntuación', 'Puntuación de usuarios'])

        if x_axis and y_axis and color_sc:
            scatter_fig = px.scatter(df_games,x=x_axis, y=y_axis, color=color_sc, hover_data=['Título'])
            scatter_fig.update_xaxes(categoryorder='category ascending').update_layout(
            yaxis_title=y_axis)
            if x_axis=="Fecha de lanzamiento":
                scatter_fig.update_xaxes(type="date")
            if y_axis=="Fecha de lanzamiento":
                scatter_fig.update_yaxes(type="date")

            scatter_fig.update_yaxes(categoryorder='category ascending')

            if x_axis=="Puntuación" or x_axis=="Puntuación de usuarios":
                if x_axis=="Puntuación":
                    bar_fig = px.histogram(df_games[df_games['Puntuación'] != 0.0],x=x_axis,  color=color_sc)
                if x_axis=="Puntuación de usuarios":
                    bar_fig = px.histogram(df_games[df_games['Puntuación de usuarios'] > 0.0],x=x_axis,  color=color_sc)
            else:
                bar_fig = px.histogram(df_games,x=x_axis,  color=color_sc)

            bar_fig.update_layout(yaxis_title="Número de títulos")

        if bar_x :

            df_pie_dinamic=df_games.groupby(bar_x).count().sort_values(by="2D", ascending=False).rename(columns = {'Título':'Nº de títulos'})

            df_pie_other=df_pie_dinamic.iloc[:,:1]
            df_pie_top=df_pie_other.head(10)

            other_row=df_pie_other.iloc[:1,:1]
            other_row["Resto"]="Resto"
            other_row[other_row.columns.to_list()[0]]=df_pie_other.tail(len(df_pie_other)-10)['Nº de títulos'].sum()
            other_row=other_row.set_index("Resto")

            df_pie_top=df_pie_top.append(other_row)
     
            fig_pie_dinamic = px.pie(df_pie_top, values='Nº de títulos', names=df_pie_top.index.values)
            fig_pie_dinamic.update_traces(textposition='inside')
            fig_pie_dinamic.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')   

        container1 = st.container()
        col1, col2 = st.columns(2)

        with container1:
            with col2:
                st.write('## Diagrama de barras por variables seleccionadas') 
                st.plotly_chart(bar_fig, use_container_width=True)                
            with col1:
                st.write('## Top 15 por dimensión seleccionada ')  
                st.plotly_chart(fig_pie_dinamic, use_container_width=True)

        cs = st.columns(1)
        with cs[0]:
            st.write('## Nube de puntos por variables seleccionadas')
            st.plotly_chart(scatter_fig, use_container_width=True)


