"""Supports the main streamlit script.
"""


import streamlit as st
import pandas as pd
import plotly.express as px


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

    with st.expander(label=f"WIN/LOSS/DRAW - {value.title()}", expanded=True):
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
    with st.expander(label=f"GAME PLY - {value.title()}", expanded=True):
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

