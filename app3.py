import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import streamlit as st
from streamlit_ace import st_ace


def app():
    display, editor = st.columns((2, 1))

    hello_world = """st.write('### Sandbox')

df=pd.read_csv("games-data-cleaned.csv")

fig = plt.figure(figsize=(10, 4))
sns.boxplot(x='platform', y = 'score', data = df)
plt.xticks(rotation=70)
plt.tight_layout()
st.pyplot(fig)"""

    with editor:
        st.write('### Edit de código')
        code = st_ace(
            value=hello_world,
            language="python",
            theme="gruvbox",
            auto_update=True,
            key="vscode"
        )
        st.write(""" Librerías disponibles
- Pandas (pd)
- Numpy (np)
- Seaborn (sns)
- Matplotlib.pyplot (plt)
- Plotly.express (px)
""")
    with display:
        exec(code)
