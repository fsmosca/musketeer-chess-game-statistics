"""The main streamlit script
"""


import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from modules.utility import win_loss_draw_stats
from modules.getdeta import get_all


st.set_page_config(
    page_title="Musketeer Chess Game Statistics",
    page_icon="🧊",
    layout="wide",
)


if 'combo_selection1' not in st.session_state:
    st.session_state.combo_selection1 = 0
if 'combo_selection2' not in st.session_state:
    st.session_state.combo_selection2 = 1
if 'endingmatcount' not in st.session_state:
    st.session_state.endingmatcount = 14
if 'middlematcount' not in st.session_state:
    st.session_state.middlematcount = 20


@st.cache
def read_data():
    return get_all()


def main():
    with st.sidebar:
        choose = option_menu("Musketeer Chess", ["About", "Game Statistics"],
                             icons=['house', 'bar-chart'],
                             menu_icon="app-indicator", default_index=0,
                             styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
        )

    if choose == "About":
        st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;}
            </style> """, unsafe_allow_html=True)

        st.markdown('<p class="font">About Musketeer Chess</p>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns([0.5, 0.1, 0.4])

        with c1:    
            st.markdown('''
            Musketeer chess invented by Zied Haddad is a modern chess variant that is played on 8x8 board but starts on 10x8 board 
            with standard chess pieces plus 2 additional piece types.
            ''')

            st.image(['musketeer_after_selection_phase.png'], width=200)

            st.markdown('''
            The players are allowed to select 2 new piece types out of 10 different piece types to choose from such as 
            Archbishop, Cannon, Chancellor, Dragon, Elephant, Fortress, Hawk, Leopard, Spider and Unicorn. The default 
            piece types are the Cannon and the Leopard and after selection players can then drop those at specific file 
            of their choice. In the given diagram the Leopard in B0 will be moved to B1 once the Knight at B1 moves to C3 or A3. 
            ''')

        with c3: 
            st.markdown('''
            #### Rules  
            * https://musketeerchess.net/p/games/musketeer/rules/rules-short.php  
            * https://musketeerchess.net/site/game-rules/
            * https://github.com/fsmosca/musketeer-chess
            ''')

            st.markdown('''
            #### Online play  
            * https://musketeerchess.net/p/games/musketeer/index.php  
            ''')


    elif choose == "Game Statistics":
        df = read_data()

        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Game Statistics</p>', unsafe_allow_html=True)  

        options = list(df['comboname'].unique())

        with st.expander(label='USER INPUT OPTIONS', expanded=True):
            with st.form(key='form'):
                c1, c2 = st.columns(2)
                with c1:
                    v1 = st.selectbox(
                        label="Select Combo Name",
                        index=st.session_state.combo_selection1,
                        options=options, key=1,
                        help='Select piece combination for comparison.')
                    st.session_state.endingmatcount = st.number_input(
                        label='End phase piece count',
                        value=14,
                        min_value=2,
                        max_value=19,
                        help='The material count from pawn to king that is '
                             'used in end phase game statistics calculations. '
                             'If material count of last position of the game '
                             'is this value or less then include such game in '
                             'the calculation. min=2, max=19, default=14'
                    )
                with c2:
                    v2 = st.selectbox(
                        label="Select Combo Name",
                        index=st.session_state.combo_selection2,
                        options=options,
                        key=2,
                        help='Select piece combination for comparison.')
                    st.session_state.middlematcount = st.number_input(
                        label='Middle phase piece count',
                        value=20,
                        min_value=20,
                        max_value=36,
                        help='The material count from pawn to king that '
                             'is used in middle phase game statistics '
                             'calculations. If material count of last '
                             'position of the game is this value or more '
                             'then include such game in the calculation. '
                             'min=20, max=36, default=20'
                    )                    
                start = st.form_submit_button(label='Generate')

        if not start:
            st.stop()
        else:
            col1, col2 = st.columns(2)
            with col1:                
                win_loss_draw_stats(df, v1)
            with col2:                
                win_loss_draw_stats(df, v2)

        with st.expander(label='OTHER INFORMATION'):
            st.markdown('''
            * The games are generated using the [stockfish musketeer](https://github.com/ianfab/Musketeer-Stockfish) engine run at TC 30s+100ms.
            ''')


if __name__ == '__main__':
    main()


