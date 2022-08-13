import streamlit as st
import pandas as pd
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report


def app():
    st.markdown("""---""") 
    df_0 = pd.read_csv("games-data-cleaned.csv")
    df=df_0.iloc[:,0:15].convert_dtypes()

    if st.checkbox("Limitar a títulos calificados"):
        df_calif=df.loc[df['score']>0]
        pr = ProfileReport(df_calif, explorative=True)
        st.header('**Dataframe**')
        st.write(df_calif.head(10))
        st.write('---')
        st.header('**Pandas Profiling Report**')
        st_profile_report(pr)
    else:
        pr = ProfileReport(df, explorative=True)
        st.header('**DataFrame**')
        st.write(df.head(10))
        st.write('---')
        st.header('**Pandas Profiling Report**')
        st.write("Number of errors generating report:")
        st.write(pr)
        st_profile_report(pr)