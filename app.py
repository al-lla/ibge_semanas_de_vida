#%%

import pandas as pd
import matplotlib.pyplot as plt
from pywaffle import Waffle
import streamlit as st

st.set_page_config(page_title='Quantas semanas você tem?')

st.write('# Hello, World!')

#%%

df = pd.read_csv('ibge.csv')
df.head()

# %%

# criar variável que aceita data de nascimento
# calcular quantas semanas foram vividas a partir de data de nascimento


idade = 25
genero = 'H'

dados = df.loc[df.idade == idade]
semanas_vida = dados.semanas_morte_homens.iloc[0]
semanas_vividas = dados.idade.iloc[0] * 52
semanas_restantes = dados.expectativa_sobrevida_homens_semanas.iloc[0]

linhas = int(semanas_vida / 52) + (semanas_vida % 52 > 0)

data = {'semanas vividas': round(semanas_vividas/semanas_vida * 100),
        'semanas restantes': round(semanas_restantes/semanas_vida * 100)}

# %%

fig = plt.figure(
    FigureClass=Waffle,
    rows=76,
    columns=52,
    values=data,
    figsize=(50, 40),
    colors=["#FCB24C", "#DDD3C3"],
    # labels=[f"{k} ({v}%)" for k, v in data.items()],
    # legend={'loc': 'lower left', 'ncol': 2, 'framealpha': 0},
    starting_location='NW',
    vertical=True
)

plt.show()
st.pyplot(fig)

# %%
