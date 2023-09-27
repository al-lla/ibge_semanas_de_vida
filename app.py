
from datetime import datetime
from dateutil import relativedelta
from PIL import Image

import pandas as pd
import matplotlib.pyplot as plt
from pywaffle import Waffle
import streamlit as st


st.set_page_config(page_title='Semanas de vida')

with st.container():

    col1, col2 = st.columns([1, 3])
    
    with col1:
        logo = Image.open('um_passo_de_cada_vez.png')
        st.image(logo.resize((150, 150)), output_format='PNG')

    with col2:
        st.write('')
        st.write('## Você sabe quantas semanas ainda tem de vida?')

    st.write('---')

@st.cache_data
def carregar_dados():
    return pd.read_csv('ibge.csv')

with st.container():
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        data_nascimento = st.date_input('Qual a sua data de nascimento?',
                                        datetime(1990, 1, 1),
                                        min_value=datetime(1940, 1, 1),
                                        max_value=datetime.today())
    
    with col2:
        genero = st.radio('Qual é o seu gênero?', ['Feminino', 'Masculino'], horizontal=True)
        st.write('<sub>* Por limitações da base do IBGE, possuímos expectativa de vida apenas para os gêneros feminino e masculino</sub>', unsafe_allow_html=True)

    hoje = datetime.today()

    diferenca_datas = relativedelta.relativedelta(hoje, data_nascimento)
    
    idade = diferenca_datas.years
    semanas_vividas = ((diferenca_datas.years * 52)
                    + (diferenca_datas.months * 4)
                    + round(diferenca_datas.days / 7))
    
    st.write('---')

with st.container():
    df = carregar_dados()
    dados = df.loc[df.idade == idade]

    if genero == 'Masculino':
        semanas_vida = dados.semanas_morte_homens.iloc[0]
    elif genero == 'Feminino':
        semanas_vida = dados.semanas_morte_mulheres.iloc[0]
    
    semanas_restantes = semanas_vida - semanas_vividas

with st.container():
    st.write(f"#### Você tem **{idade} anos** e já viveu **{semanas_vividas} semanas**!")
    st.write(f"Segundo os dados do IBGE, espera-se que você viva **{semanas_vida} semanas**, o que resulta em **{semanas_restantes} semanas restantes**.")

with st.container():

    linhas = int(semanas_vida / 52) + (semanas_vida % 52 > 0)

    data = {'semanas vividas': round(semanas_vividas/semanas_vida * 100),
            'semanas restantes': round(semanas_restantes/semanas_vida * 100)}

    fig = plt.figure(
        FigureClass=Waffle,
        rows=linhas,
        columns=52,
        values=data,
        figsize=(50, 40),
        colors=["#FCB24C", "#DDD3C3"],
        labels=[f"{k} ({v}%)" for k, v in data.items()],
        legend={'loc': 'upper right',
                'bbox_to_anchor': (1, 1.03),
                'ncol': len(data),
                'fontsize': 30,
                'framealpha': 0},
        starting_location='NW',
        vertical=True
    )

    st.pyplot(fig)

with st.container():
    st.write('---')
    st.write('Essa visualização é inspirada em um [texto](https://open.substack.com/pub/alexandrealves/p/voce-ja-parou-para-pensar-em-quanto?r=28qyby&utm_campaign=post&utm_medium=web) de minha newsletter e em um [post](https://www.linkedin.com/posts/alexandre-ll-alves_voc%C3%AA-j%C3%A1-parou-para-pensar-em-quanto-tempo-activity-7110998566822658049-mqPe?utm_source=share&utm_medium=member_desktop) que escrevi no Linked In.')

