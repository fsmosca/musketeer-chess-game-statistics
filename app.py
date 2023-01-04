"""The main streamlit script
"""


import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px


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
def read_data(fn):
    df = pd.read_csv(fn)
    return df


def results(dfc, filter=None):
    if filter is None:
        res = '1-0'
        dfwwins = dfc[dfc['result'] == res]
        wwins = len(dfwwins)

        res = '0-1'
        dfbwins = dfc[dfc['result'] == res]
        bwins = len(dfbwins)

        res = '1/2-1/2'
        dfdraws = dfc[dfc['result'] == res]
        draws = len(dfdraws)
        return wwins, bwins, draws, wwins + bwins + draws

    elif filter == 'end':
        res = '1-0'
        ndf = dfc[(dfc['result'] == res) & (dfc['pcscnt'] <= st.session_state.endingmatcount)]
        wwins = len(ndf)

        res = '0-1'
        ndf = dfc[(dfc['result'] == res) & (dfc['pcscnt'] <= st.session_state.endingmatcount)]
        bwins = len(ndf)

        res = '1/2-1/2'
        ndf = dfc[(dfc['result'] == res) & (dfc['pcscnt'] <= st.session_state.endingmatcount)]
        draws = len(ndf)
        return wwins, bwins, draws, wwins + bwins + draws

    elif filter == 'middle':
        res = '1-0'
        ndf = dfc[(dfc['result'] == res) & (dfc['pcscnt'] >= st.session_state.middlematcount)]
        wwins = len(ndf)

        res = '0-1'
        ndf = dfc[(dfc['result'] == res) & (dfc['pcscnt'] >= st.session_state.middlematcount)]
        bwins = len(ndf)

        res = '1/2-1/2'
        ndf = dfc[(dfc['result'] == res) & (dfc['pcscnt'] >= st.session_state.middlematcount)]
        draws = len(ndf)
        return wwins, bwins, draws, wwins + bwins + draws   

    elif filter == 'pawnless':
        res = '1-0'
        ndf = dfc[(dfc['result'] == res) & (dfc['pacnt'] == 0)]
        wwins = len(ndf)
        res = '0-1'
        ndf = dfc[(dfc['result'] == res) & (dfc['pacnt'] == 0)]
        bwins = len(ndf)
        res = '1/2-1/2'
        ndf = dfc[(dfc['result'] == res) & (dfc['pacnt'] == 0)]
        draws = len(ndf)
        return wwins, bwins, draws, wwins + bwins + draws


def win_loss_draw_stats(df, value):
    dfc = df[df['comboname'] == value]
    wwins, bwins, draws, games = results(dfc, filter=None)

    d = {
        'result': ['wwins', 'bwins', 'draws'],
        'comboname': [value, value, value],
        'count': [wwins, bwins, draws],
        'pct': [f'{wwins} ({round(100*wwins/games, 2)}%)', f'{bwins} ({round(100*bwins/games, 2)}%)', f'{draws} ({round(100*draws/games, 2)}%)']
    }

    df1 = pd.DataFrame(d)

    with st.expander(label=f"WIN/LOSS/DRAW - {value.title()}", expanded=False):
        st.markdown(f'''
        total_games = **{games}**  
        ''')

        fig = px.bar(df1, y='result', x='count', color='result', orientation='h', height=250, text='pct')
        fig.update_layout(
            margin=dict(b=10),
            font_size=14
        )
        with st.container():
            st.plotly_chart(fig, use_container_width=True)

    # Show move number stats such as min, max, mean and stdev of game plies.
    mingameply = dfc['plycnt'].min()
    maxgameply = dfc['plycnt'].max()
    meangameply = dfc['plycnt'].mean()
    mediangameply = dfc['plycnt'].median()
    stdevgameply = dfc['plycnt'].std()

    d3 = {
        'name': ['min', 'max', 'mean', 'median', 'stdev'],
        'game plycnt': [round(mingameply), round(maxgameply), round(meangameply), round(mediangameply), round(stdevgameply)]
    }
    df3 = pd.DataFrame(d3)
    with st.expander(label=f"GAME PLY - {value.title()}", expanded=False):
        fig = px.bar(df3, y='name', x='game plycnt', color='name', orientation='h', width=650, height=350, text_auto=True)
        fig.update_layout(
            margin=dict(b=10),
            font_size=14
        )        
        st.plotly_chart(fig, use_container_width=True)

        fig = px.histogram(dfc, x='plycnt', height=350,
            labels={
                'plycnt': 'game plycnt'}
            )
        fig.update_layout(
            margin=dict(b=10),
            font_size=14
        )            
        st.plotly_chart(fig, use_container_width=True)

    # End Phase
    wwins, bwins, draws, games = results(dfc, filter='end')

    d = {
        'result': ['wwins', 'bwins', 'draws'],
        'comboname': [value, value, value],
        'count': [wwins, bwins, draws],
        'pct': [f'{wwins} ({round(100*wwins/games, 2)}%)', f'{bwins} ({round(100*bwins/games, 2)}%)', f'{draws} ({round(100*draws/games, 2)}%)']
    }

    df1 = pd.DataFrame(d)

    with st.expander(label=f"END PHASE WIN/LOSS/DRAW - {value.title()}", expanded=False):
        st.markdown(f'''
        material_count = **{st.session_state.endingmatcount}** or less  
        total_games = **2704**  
        end phase games = **{games} ({100*games/2704:0.2f}%)**
        ''')
        fig = px.bar(df1, y='result', x='count', color='result', orientation='h', height=250, text='pct')
        fig.update_layout(
            margin=dict(b=10),
            font_size=14
        )        
        with st.container():
            st.plotly_chart(fig, use_container_width=True)

    # Middle Phase
    wwins, bwins, draws, games = results(dfc, filter='middle')

    d = {
        'result': ['wwins', 'bwins', 'draws'],
        'comboname': [value, value, value],
        'count': [wwins, bwins, draws],
        'pct': [f'{wwins} ({round(100*wwins/games, 2)}%)', f'{bwins} ({round(100*bwins/games, 2)}%)', f'{draws} ({round(100*draws/games, 2)}%)']
    }

    df1 = pd.DataFrame(d)

    with st.expander(label=f"MIDDLE PHASE WIN/LOSS/DRAW - {value.title()}", expanded=False):
        st.markdown(f'''
        material_count = **{st.session_state.middlematcount}** or more  
        total_games = **2704**  
        middle phase games = **{games} ({100*games/2704:0.2f}%)**
        ''')
        fig = px.bar(df1, y='result', x='count', color='result', orientation='h', height=250, text='pct')
        fig.update_layout(
            margin=dict(b=10),
            font_size=14
        )        
        with st.container():
            st.plotly_chart(fig, use_container_width=True)

    # Pawnless ending
    wwins, bwins, draws, games = results(dfc, filter='pawnless')

    d = {
        'result': ['wwins', 'bwins', 'draws'],
        'comboname': [value, value, value],
        'count': [wwins, bwins, draws],
        'pct': [f'{wwins} ({round(100*wwins/games, 2)}%)', f'{bwins} ({round(100*bwins/games, 2)}%)', f'{draws} ({round(100*draws/games, 2)}%)']
    }

    df1 = pd.DataFrame(d)

    with st.expander(label=f"PAWNLESS WIN/LOSS/DRAW - {value.title()}", expanded=False):
        st.markdown(f'''
        total_games = **2704**  
        pawnless games = **{games} ({100*games/2704:0.2f}%)**
        ''')
        fig = px.bar(df1, y='result', x='count', color='result', orientation='h', height=250, text='pct')
        fig.update_layout(
            margin=dict(b=10),
            font_size=14
        )        
        with st.container():
            st.plotly_chart(fig, use_container_width=True)


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
        df = read_data('musketeer_chess_data.csv')

        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Game Statistics</p>', unsafe_allow_html=True)  

        options = list(df['comboname'].unique())

        with st.expander(label='USER INPUT OPTIONS', expanded=True):
            with st.form(key='form'):
                c1, c2 = st.columns(2)
                with c1:
                    v1 = st.selectbox(label="Select Combo Name", index=st.session_state.combo_selection1, options=options, key=1,
                                      help='Select piece combination for comparison.')
                    st.session_state.endingmatcount = st.number_input(
                        label='End phase piece count',
                        value=14,
                        min_value=2,
                        max_value=19,
                        help='The material count from pawn to king that is used in end phase game statistics calculations. If material count of last position of the game '
                              'is this value or less then include such game in the calculation. min=2, max=19, default=14'
                    )
                with c2:
                    v2 = st.selectbox(label="Select Combo Name", index=st.session_state.combo_selection2, options=options, key=2,
                                      help='Select piece combination for comparison.')
                    st.session_state.middlematcount = st.number_input(
                        label='Middle phase piece count',
                        value=20,
                        min_value=20,
                        max_value=36,
                        help='The material count from pawn to king that is used in middle phase game statistics calculations. If material count of last position of the game '
                              'is this value or more then include such game in the calculation. min=20, max=36, default=20'
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
            st.markdown(f'''
            * The games are generated using the [stockfish musketeer](https://github.com/ianfab/Musketeer-Stockfish) engine run at TC 30s+100ms.
            ''')


if __name__ == '__main__':
    main()


