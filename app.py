
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
        data_nascimento1 = st.date_input('Qual é a sua data de nascimento?',
                                         datetime(1990, 1, 1),
                                         min_value=datetime(1940, 1, 1),
                                         max_value=datetime.today())
    
    with col2:
        sexo1 = st.radio('Qual é o seu sexo?', ['Feminino', 'Masculino'], horizontal=True)

    if on:
        col1, col2 = st.columns(2)
    
        with col1:
            data_nascimento2 = st.date_input('Qual a data de nascimento da segunda pessoa?',
                                            datetime(1990, 1, 1),
                                            min_value=datetime(1940, 1, 1),
                                            max_value=datetime.today())
        
        with col2:
            sexo2 = st.radio('Qual é o sexo da segunda pessoa?', ['Feminino', 'Masculino'], horizontal=True)        

    submit = st.form_submit_button('Carregar dados', type='primary')

if submit:

    with st.container():

        hoje = datetime.today()

        diferenca_datas1 = relativedelta.relativedelta(hoje, data_nascimento1)
        idade1 = diferenca_datas1.years
        semanas_vividas1 = ((diferenca_datas1.years * 52)
                            + (diferenca_datas1.months * 4)
                            + round(diferenca_datas1.days / 7))

        if on:
            diferenca_datas2 = relativedelta.relativedelta(hoje, data_nascimento2)       
            idade2 = diferenca_datas2.years
            semanas_vividas2 = ((diferenca_datas2.years * 52)
                                + (diferenca_datas2.months * 4)
                                + round(diferenca_datas2.days / 7))
            
        df = carregar_dados()

        if on:
            dados = df.loc[(df.idade == idade1)
                           | (df.idade == idade2)]
        else:
            dados = df.loc[df.idade == idade1]
            
        if sexo1 == 'Masculino':
            semanas_vida1 = dados[dados.index == idade1].semanas_morte_homens.iloc[0]

        elif sexo1 == 'Feminino':
            semanas_vida1 = dados[dados.index == idade1].semanas_morte_mulheres.iloc[0]

        semanas_restantes1 = semanas_vida1 - semanas_vividas1        
        
        if on:
            
            if sexo2 == 'Masculino':
                semanas_vida2 = dados[dados.index == idade2].semanas_morte_homens.iloc[0]

            elif sexo2 == 'Feminino':
                semanas_vida2 = dados[dados.index == idade2].semanas_morte_mulheres.iloc[0]

            semanas_restantes2 = semanas_vida2 - semanas_vividas2

        if on:
            semanas_interseccao = int(min(semanas_restantes1, semanas_restantes2))
            semanas_extras = int(max(semanas_restantes1, semanas_restantes2) - semanas_interseccao)

    with st.container():
        st.write(f"#### Você tem {idade1} anos e já viveu {semanas_vividas1} semanas!")
        st.write(f"Segundo os dados do IBGE, espera-se que você viva {'' if on else '**'}{semanas_vida1} semanas{'' if on else '**'}, o que resulta em {'' if on else '**'}{semanas_restantes1} semanas restantes{'' if on else '**'}.")

        colunas = int(semanas_vida1 / 52) + (semanas_vida1 % 52 > 0)
        data = {'semanas vividas': round(semanas_vividas1/semanas_vida1 * 100),
                'semanas restantes': round(semanas_restantes1/semanas_vida1 * 100)}

        if on:
            st.write(f"A pessoa com que você está se comparando, possui {idade2} anos e já viveu {semanas_vividas2} semanas. Espera-se que ela viva {semanas_vida2} semanas.")

            dias_data_nascimento1 = diferenca_datas1.years*365 + diferenca_datas1.months*30 + diferenca_datas1.days
            dias_data_nascimento2 = diferenca_datas2.years*365 + diferenca_datas2.months*30 + diferenca_datas2.days

            if dias_data_nascimento1 != dias_data_nascimento2:

                diferenca_nascimentos = relativedelta.relativedelta(max(data_nascimento1, data_nascimento2), min(data_nascimento1, data_nascimento2))       
                semanas_antes = ((diferenca_nascimentos.years * 52)
                                + (diferenca_nascimentos.months * 4)
                                + round(diferenca_nascimentos.days / 7))

                total_semanas = max(semanas_vida1, semanas_vida2) + semanas_extras
                colunas = int(total_semanas / 52) + (total_semanas % 52 > 0)

                if dias_data_nascimento1 > dias_data_nascimento2:
                    data = {'suas semanas vividas sozinho': round(semanas_antes/total_semanas * 100),
                            'suas semanas vividas em conjunto': round((semanas_vividas1-semanas_antes)/total_semanas * 100),
                            'semanas em conjunto restantes': round(semanas_interseccao/total_semanas * 100)}

                else:
                    data = {'semanas da segunda pessoa vividas sozinha': round(semanas_antes/total_semanas * 100),
                            'suas semanas vividas em conjunto': round((semanas_vividas2-semanas_antes)/total_semanas * 100),
                            'semanas em conjunto restantes': round(semanas_interseccao/total_semanas * 100)}

            else:
                data = {}

            if semanas_restantes1 > semanas_restantes2:

                data.update({'suas semanas sozinho': round(semanas_extras/total_semanas * 100)})

                st.write(f"Isso significa que vocês possuem mais **{semanas_interseccao} semanas em conjunto** e você terá **{semanas_extras} semanas de vida a mais** que a segunda pessoa.")

            elif semanas_restantes2 > semanas_restantes1:

                data.update({'semanas da segunda pessoa sozinha': round(semanas_extras/total_semanas * 100)})

                st.write(f"Isso significa que vocês possuem mais **{semanas_interseccao} semanas em conjunto** e a segunda pessoa terá **{semanas_extras} semanas de vida a mais** que você.")

            else:

                data.update({'semanas vividas em conjunto': round(semanas_vividas1/semanas_vida1 * 100),
                             'semanas em conjunto restantes': round(semanas_interseccao/semanas_vida1 * 100)})
                
                st.write(f"Isso significa que vocês possuem mais **{semanas_interseccao} semanas em conjunto**.")

    with st.container():

        cores = ['#60D394', '#FCB24C', '#DDD3C3', '#F68482']
        
        if len(data) <= 2:
            posicao_legenda = (1, 1.05)
        else:
            posicao_legenda = (1, 1.1)

        fig = plt.figure(
            FigureClass=Waffle,
            rows=52,
            columns=colunas,
            values=data,
            figsize=(50, 40),
            colors=cores[0:len(data)],
            labels=[f"{k} ({v}%)" for k, v in data.items()],
            legend={'loc': 'upper right',
                    'bbox_to_anchor': posicao_legenda,
                    'ncol': 2,
                    'fontsize': 40,
                    'framealpha': 0},
            starting_location='NW',
            vertical=True
        )

        st.pyplot(fig)

    with st.container():
            st.write('---')
            st.write('Essa visualização é inspirada em um [texto](https://open.substack.com/pub/alexandrealves/p/voce-ja-parou-para-pensar-em-quanto?r=28qyby&utm_campaign=post&utm_medium=web) de minha newsletter e em um [post](https://www.linkedin.com/posts/alexandre-ll-alves_voc%C3%AA-j%C3%A1-parou-para-pensar-em-quanto-tempo-activity-7110998566822658049-mqPe?utm_source=share&utm_medium=member_desktop) que escrevi no Linked In.')
