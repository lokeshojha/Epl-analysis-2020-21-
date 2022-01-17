import streamlit as st
import pandas as pd
import helper
import plotly.graph_objects as go
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
#from helper import ComplexRadar
from functools import reduce



st.sidebar.title('Premier-League:2020-21')

st.sidebar.image('https://cdnuploads.aa.com.tr/uploads/Contents/2021/08/13/thumbs_b_c_d391bd815724afbe9b49e0879b86ff38.jpg?v=210138')

user_menu=st.sidebar.radio(
    'Select an option',
    ('PL Table' ,'Overall Analysis','Team wise Analysis', 'Player wise Analysis')
)
teams=pd.read_csv('pl-1.csv',encoding= 'unicode_escape')
standard_stats=pd.read_csv('pl-2.csv')
goal_shot_creation=pd.read_csv('pl-3.csv',encoding= 'latin-1')
teams_shooting=pd.read_csv('pl-4.csv')

players=pd.read_csv('players.csv',encoding= 'latin-1',index_col=False)
player_shooting = pd.read_csv('player_shooting.csv',encoding='latin-1')
defence = pd.read_csv('player_defence.csv',encoding='latin-1',index_col=False)
pass_types = pd.read_csv('pass_types.csv',encoding='latin-1',index_col=False)
passing = pd.read_csv('player_passing.csv',encoding='latin-1',index_col=False)
goals_shot=pd.read_csv('Goal_shot_actions.csv',encoding='latin-1',index_col=False)
poss = pd.read_csv('player_poss.csv',encoding='latin-1',index_col=False)

player_shooting['Player']=player_shooting['Player'].apply(lambda x:x.split("\\")[0])
players['Player']=players['Player'].apply(lambda x:x.split('\\')[0])
#players['Nation'] = players['Nation'].apply(lambda x:x.split()[-1])
defence['Player']=defence['Player'].apply(lambda x:x.split('\\')[0])
pass_types['Player']=pass_types['Player'].apply(lambda x:x.split('\\')[0])
passing['Player']=passing['Player'].apply(lambda x:x.split('\\')[0])
goals_shot['Player']=goals_shot['Player'].apply(lambda x:x.split("\\")[0])
poss['Player'] = poss['Player'].apply(lambda x:x.split("\\")[0])


if (user_menu=='PL Table'):
    st.sidebar.header('Points Table')
    #st.table(teams)
    teams.rename(columns={'Rk': 'Rank', 'Squad': 'Club'}, inplace = True)
    teams_new = teams[['Rank', 'Club', 'Matches', 'Win', 'Draw', 'Loss', 'GF', 'GA', 'GD', 'Points']]
    #teams.reset_index(drop=True, inplace=True)
    st.table(teams_new)

#-----------------------------------------------overall analysis----------------
if(user_menu=='Overall Analysis'):
    st.sidebar.header('overall stats')
    scorer = helper.top_scorer(players)
    my_list=['Top Scorer','Top Assist','Teams with most goals','Most Goals scored',"Team's average Age",
             "goals vs expected goals", "Penalty Kicks awarded", "Red cards and Yellow cards","Possessions"]
    selected_option = st.sidebar.selectbox("Select option", my_list)


    if (selected_option == 'Top Scorer'):

        st.header('Top Scorer')
        scorer = helper.top_scorer(players)
        st.table(scorer)

    if(selected_option== 'Top Assist'):
        st.header('Top Assist')
        assists = helper.top_assist(players)
        st.table(assists)

    if(selected_option=='Teams with most goals'):
        st.header('Teams with most goals')
        goals_for, goals_conceded = helper.team_goals(teams)
        st.table(goals_for)


    if (selected_option == "Team's average Age"):
        st.header("Team's average Age")
        average_age = helper.average_age(standard_stats)
        st.table(average_age)
        x=standard_stats['Age'].sort_values(ascending = False)
        fig = px.bar(standard_stats, x,  y="Squad", orientation='h', width=800, height=600)
        st.plotly_chart(fig)

    if(selected_option == 'goals vs expected goals'):
        st.header("goals vs expected goals")
        helper.abcd(standard_stats)

    if(selected_option == "Penalty Kicks awarded"):
        st.header("Penalty kicks awarded")
        helper.penalty(standard_stats)

    if (selected_option == "Red cards and Yellow cards"):
        st.header("Red Cards and Yellow Cards")
        helper.cards(standard_stats)

    if (selected_option == "Possessions"):
        st.header("Possessions")
        helper.Possessions(standard_stats)



#-----------------------------------------------Team wise analysis------------------------------------------------------

if(user_menu=='Team wise Analysis'):
    teams_list = teams['Squad'].sort_values().values.tolist()
    selected_team = st.sidebar.selectbox("Select option", teams_list)

    selected_option = st.selectbox(
        'Select an option',
        ('Top 5 Goal Scorer','Top Assists','*'))

    if(selected_option == 'Top 5 Goal Scorer'):
        top_scorers = helper.top_goal_scorer(selected_team, players)
        st.table(top_scorers)

    if(selected_option == 'Top Assists'):
        top_assists = helper.top_assists(selected_team, players)
        st.table(top_assists)

# --------------------------------------------Player wise analysis---------------------------------

if(user_menu=='Player wise Analysis'):
    options = ['Player vs Player','Assist Per 90 vs Assists Per 90', 'xg vs gls', 'XG vs Final Third', 'Player vs Player2']
    selected_option = st.selectbox('Select an option ', options)

    if selected_option == 'Assist Per 90 vs Assists Per 90' :
        temp_df = players[players['Min'] > 1500]
        temp_df = temp_df[['Player', 'Ast_P90', 'xA_P90']].sort_values('xA_P90', ascending=False)

        fig = px.scatter(temp_df, x="Ast_P90", y="xA_P90", hover_data=['Player'])
        st.plotly_chart(fig)

    if selected_option == 'xg vs gls' :
        temp_df = players[players['Min'] > 1500]
        temp_df = temp_df[['Player', 'Gls_P90', 'xG_P90']].sort_values('xG_P90', ascending=False)

        fig = px.scatter(temp_df, x="Gls_P90", y="xG_P90", hover_data=['Player'])
        st.plotly_chart(fig)

    # XG VS FINAL THIRD -------------------


    if selected_option == 'Player vs Player':
        player_list = player_shooting['Player'].sort_values().values.tolist()
        player1 = st.selectbox("Select Player 1", player_list, key='hi')
        player2 = st.selectbox("Select Player 2", player_list)
        playernames = [player1,player2]
        variables = ['xG', '90s', 'SoT%', 'Dist']
        ranges = [(0, 25), (0, 40), (0, 80), (0, 30)]
        fig1 = plt.figure(figsize=(6, 6))
        radar = helper.ComplexRadar(fig1, variables, ranges)
        for player_name in playernames:
            data = list(helper.get_player_stats(player_shooting, player_name))
            radar.plot(data, label=player_name)
            radar.fill(data, alpha=0.2)
        radar.ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10),
                        fancybox=True, shadow=True, ncol=4, fontsize=13)
        # plt.show()
        st.pyplot(fig1)

    if selected_option == 'Player vs Player2':
        shoot_temp = player_shooting
        merged_df1 = pd.merge(shoot_temp,players, on= 'Player',how= 'inner')
        merged_df2 = pd.merge(merged_df1, goals_shot, on="Player",how='inner')

        merged_df3 = pd.merge(pass_types, passing, on="Player", how='inner')
        merged_df4 = pd.merge(merged_df3,defence, on="Player", how='inner')

        merged_df5= pd.merge(merged_df2,merged_df4,on="Player", how='inner')
        merged_df6 = pd.merge(merged_df5, poss, on="Player", how='inner')

        all_df = merged_df6
        st.table(all_df.head(2))
        st.header(all_df.shape)

        range_dict = {'G/Sh': (0, 1.00),
                      'npxG+xA_P90': (0, 1.00),
                      'xA_P90': (0, 1.00),
                      'npxG_P90': (0, 1.00),
                      'xA_P90': (0, 1.00),
                      'T_PrgDist': (0, 20000),
                      'L_Cmp': (0, 500),
                      'L_Prog': (0, 300),
                      'CrsPA': (0, 35),
                      'SCA90': (0, 7.00),
                      'GCA90': (0, 1.00),
                      'S_PassLive': (0, 130),
                      'G_PassLive': (0, 25),
                      'S_Drib': (0, 25),
                      'Press_x': (0, 500),
                      'Passes_Cmp': (0, 3000),
                      'Final_Third': (0, 120),
                      'Att Pen': (0, 350),
                      'TotDist': (0, 15000),
                      'T_Tkl': (0, 130),
                      'T_Att 3rd': (0, 25),
                      'Succ_x': (0, 250),   #_x
                      'Press_Mid_3rd': (0, 450),
                      'Press_Att_3rd': (0, 450),
                      'Block_ball': (0, 130),
                      'Int': (0, 100),
                      'Err': (0, 15)
        }

        o1 = 'G/Sh'
        o2 = 'npxG+xA_P90'
        o3 = 'xA_P90'
        o4 = 'npxG_P90'
        o5 = 'xA_P90'
        o6 = 'T_PrgDist'
        o7 = 'L_Cmp'
        o8 = 'L_Prog'
        o9 = 'CrsPA'
        o10 = 'SCA90'
        o11 = 'GCA90'
        o12 = 'S_PassLive'
        o13 = 'G_PassLive'
        o14 = 'S_Drib'
        o15 = 'Press_x'
        o16 = 'Passes_Cmp'
        o17 = 'Final_Third'
        o18 = 'Att Pen'
        o19 = 'TotDist'
        o20 = 'T_Tkl'
        o21 = 'T_Att 3rd'
        o22 = 'Succ_x'
        o23 = 'Press_Mid_3rd'
        o24 = 'Press_Att_3rd'
        o25 = 'Block_ball'
        o26 = 'Int'
        o27 = 'Err'

        l = [o1, o2, o3, o4, o5, o16, o7, o8, o9, o10, o11, o12, o13, o14, o15, o16, o17, o18, o19, o20, o21,
             o22, o23, o24, o25, o26, o27]
        ranges = []
        for i in l:
            ranges.append(range_dict[i])

        st.header(ranges)
        st.header(('range_dict'))
        st.header(range_dict)

        player_list = player_shooting['Player'].sort_values().values.tolist()
        player1 = st.selectbox("Select Player 1", player_list, key='hi')
        player2 = st.selectbox("Select Player 2", player_list)
        playernames = [player1, player2]
        option1 = st.selectbox('select option 1', l, key='key1')
        option2 = st.selectbox('select option 2', l, key='key2')
        option3 = st.selectbox('select option 3', l, key='key3')
        option4 = st.selectbox('select option 4', l, key='key4')
        option5 = st.selectbox('select option 5', l, key='key5')
        option6 = st.selectbox('select option 6', l, key='key6')
        variables = [option1,option2,option3,option4,option5,option6]
        ranges2=[range_dict[option1],range_dict[option2],range_dict[option3],range_dict[option4],
        range_dict[option5],range_dict[option6]]
        st.header(ranges2)

        fig1 = plt.figure(figsize=(6, 6))
        radar = helper.ComplexRadar(fig1, variables, ranges2)
        for player_name in playernames:
            data = list(helper.get_player_stats2(all_df, player_name, variables))
            radar.plot(data, label=player_name)
            radar.fill(data, alpha=0.2)
        radar.ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10),
                        fancybox=True, shadow=True, ncol=4, fontsize=13)
        # plt.show()
        st.pyplot(fig1)






