
from time import sleep
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
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pass
    
    with col2:
        pass
    
    with col3:
        on = st.toggle('Comparar duas pessoas')

with st.form('formulario'):

    col1, col2 = st.columns(2)
    
    with col1:
        data_nascimento1 = st.date_input('Qual a data de nascimento?',
                                         datetime(1990, 1, 1),
                                         min_value=datetime(1940, 1, 1),
                                         max_value=datetime.today())
    
    with col2:
        sexo1 = st.radio('Qual é o sexo?', ['Feminino', 'Masculino'], horizontal=True)

    if on:
        col1, col2 = st.columns(2)
    
        with col1:
            data_nascimento2 = st.date_input('Qual a data de nascimento da segunda pessoa?',
                                            datetime(1990, 1, 1),
                                            min_value=datetime(1940, 1, 1),
                                            max_value=datetime.today())
        
        with col2:
            sexo2 = st.radio('Qual é o sexo da segunda pessoa?', ['Feminino', 'Masculino'], horizontal=True)        

    submit = st.form_submit_button('Carregar dados')

if submit:

    if on == False:

        with st.container():

            hoje = datetime.today()

            diferenca_datas = relativedelta.relativedelta(hoje, data_nascimento1)
            
            idade = diferenca_datas.years
            semanas_vividas = ((diferenca_datas.years * 52)
                            + (diferenca_datas.months * 4)
                            + round(diferenca_datas.days / 7))
            
            df = carregar_dados()
            dados = df.loc[df.idade == idade]

            if sexo1 == 'Masculino':
                semanas_vida = dados.semanas_morte_homens.iloc[0]
            elif sexo1 == 'Feminino':
                semanas_vida = dados.semanas_morte_mulheres.iloc[0]
            
            semanas_restantes = semanas_vida - semanas_vividas

        with st.container():
            st.write(f"#### Você tem **{idade} anos** e já viveu **{semanas_vividas} semanas**!")
            st.write(f"Segundo os dados do IBGE, espera-se que você viva **{semanas_vida} semanas**, o que resulta em **{semanas_restantes} semanas restantes**.")

        with st.container():

            colunas = int(semanas_vida / 52) + (semanas_vida % 52 > 0)

            data = {'semanas vividas': round(semanas_vividas/semanas_vida * 100),
                    'semanas restantes': round(semanas_restantes/semanas_vida * 100)}

            fig = plt.figure(
                FigureClass=Waffle,
                rows=52,
                columns=colunas,
                values=data,
                figsize=(50, 40),
                colors=["#FCB24C", "#DDD3C3"],
                labels=[f"{k} ({v}%)" for k, v in data.items()],
                legend={'loc': 'upper right',
                        'bbox_to_anchor': (1, 1.05),
                        'ncol': len(data),
                        'fontsize': 45,
                        'framealpha': 0},
                starting_location='NW',
                vertical=True
            )

            st.pyplot(fig)

        with st.container():
            st.write('---')
            st.write('Essa visualização é inspirada em um [texto](https://open.substack.com/pub/alexandrealves/p/voce-ja-parou-para-pensar-em-quanto?r=28qyby&utm_campaign=post&utm_medium=web) de minha newsletter e em um [post](https://www.linkedin.com/posts/alexandre-ll-alves_voc%C3%AA-j%C3%A1-parou-para-pensar-em-quanto-tempo-activity-7110998566822658049-mqPe?utm_source=share&utm_medium=member_desktop) que escrevi no Linked In.')

    else:
        st.write('não desenvolvido ):')