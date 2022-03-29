"""
app.py

requirements.txt:
    streamlit==1.8.0
    streamlit-option-menu==0.3.2
    plotly==5.6.0
    parquet==1.3.1
    click==8.0.4

Note:
To fix the bug on click use the following module:
click==8.0.4
"""


from functools import cache
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


@cache
def read_data(fn):
    df = pd.read_parquet(fn)
    return df


def results(dfc, filter=None):
    if filter is None:
        res = '1-0'
        dfwwins = dfc[dfc['result'] == res]
        wwins = len(dfwwins.groupby(['comboname', 'gamekey']))

        res = '0-1'
        dfbwins = dfc[dfc['result'] == res]
        bwins = len(dfbwins.groupby(['comboname', 'gamekey']))

        res = '1/2-1/2'
        dfdraws = dfc[dfc['result'] == res]
        draws = len(dfdraws.groupby(['comboname', 'gamekey']))

        return wwins, bwins, draws, wwins + bwins + draws
    elif filter == 'end':
        res = '1-0'
        ndf = dfc[(dfc['result'] == res) & (dfc['lastpos'] == 1) & (dfc['pcscnt'] <= st.session_state.endingmatcount - 2)]
        wwins = len(ndf.groupby(['comboname', 'gamekey']))

        res = '0-1'
        ndf = dfc[(dfc['result'] == res) & (dfc['lastpos'] == 1) & (dfc['pcscnt'] <= st.session_state.endingmatcount - 2)]
        bwins = len(ndf.groupby(['comboname', 'gamekey']))

        res = '1/2-1/2'
        ndf = dfc[(dfc['result'] == res) & (dfc['lastpos'] == 1) & (dfc['pcscnt'] <= st.session_state.endingmatcount - 2)]
        draws = len(ndf.groupby(['comboname', 'gamekey']))

        return wwins, bwins, draws, wwins + bwins + draws
    elif filter == 'middle':
        res = '1-0'
        ndf = dfc[(dfc['result'] == res) & (dfc['lastpos'] == 1) & (dfc['pcscnt'] >= st.session_state.middlematcount - 2)]
        wwins = len(ndf.groupby(['comboname', 'gamekey']))

        res = '0-1'
        ndf = dfc[(dfc['result'] == res) & (dfc['lastpos'] == 1) & (dfc['pcscnt'] >= st.session_state.middlematcount - 2)]
        bwins = len(ndf.groupby(['comboname', 'gamekey']))

        res = '1/2-1/2'
        ndf = dfc[(dfc['result'] == res) & (dfc['lastpos'] == 1) & (dfc['pcscnt'] >= st.session_state.middlematcount - 2)]
        draws = len(ndf.groupby(['comboname', 'gamekey']))

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

    with st.expander(label=f"WIN/LOSS/DRAW - {value.title()}", expanded=True):
        st.markdown(f'''
        total_games = **{games}**  
        ''')

        fig = px.bar(df1, y='result', x='count', color='result', orientation='h', height=300, text='pct')
        fig.update_layout(
            margin=dict(b=10),
        )
        with st.container():
            st.plotly_chart(fig, use_container_width=True)

    # Show move number stats such as min, max, mean and stdev of game plies.
    f = {'plycnt': 'first'}
    dfgply = dfc.groupby(['gamekey'], as_index=False).agg(f)

    mingameply = dfgply['plycnt'].min()
    maxgameply = dfgply['plycnt'].max()
    meangameply = dfgply['plycnt'].mean()
    mediangameply = dfgply['plycnt'].median()
    stdevgameply = dfgply['plycnt'].std()

    d3 = {
        'name': ['min', 'max', 'mean', 'median', 'stdev'],
        'game plycnt': [round(mingameply), round(maxgameply), round(meangameply), round(mediangameply), round(stdevgameply)]
    }
    df3 = pd.DataFrame(d3)
    with st.expander(label=f"GAME PLY - {value.title()}", expanded=True):
        fig = px.bar(df3, y='name', x='game plycnt', color='name', orientation='h', height=400, text_auto=True)
        fig.update_layout(
            margin=dict(b=10),
        )        
        st.plotly_chart(fig, use_container_width=True)

        fig = px.histogram(dfgply, x='plycnt', height=400,
            labels={
                'plycnt': 'game plycnt'}
            )
        fig.update_layout(
            margin=dict(b=10),
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

    with st.expander(label=f"END PHASE WIN/LOSS/DRAW - {value.title()}", expanded=True):
        st.markdown(f'''
        material_count = **{st.session_state.endingmatcount}** or less  
        total_games = **2704**  
        end phase games = **{games} ({100*games/2704:0.2f}%)**
        ''')
        fig = px.bar(df1, y='result', x='count', color='result', orientation='h', height=300, text='pct')
        fig.update_layout(
            margin=dict(b=10),
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

    with st.expander(label=f"MIDDLE PHASE WIN/LOSS/DRAW - {value.title()}", expanded=True):
        st.markdown(f'''
        material_count = **{st.session_state.middlematcount}** or more  
        total_games = **2704**  
        middle phase games = **{games} ({100*games/2704:0.2f}%)**
        ''')
        fig = px.bar(df1, y='result', x='count', color='result', orientation='h', height=300, text='pct')
        fig.update_layout(
            margin=dict(b=10),
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
            new piece types are the cannon and the leopard.
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
        df = read_data('df.parquet.gzip')

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
                        max_value=14,
                        help='The material count from pawn to king that is used in end phase game statistics calculations. If material count of last position of the game '
                              'is this value or less then include such game in the calculation. min=2, max=14, default=14'
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


