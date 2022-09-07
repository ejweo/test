import pandas as pd
import json
from mplsoccer.pitch import Pitch
from mplsoccer import VerticalPitch
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt


def soccer_main(st):
    st.subheader('축구')
    #competitions = pd.read_json('../json/data/competitions.json')
    #st.write(competitions[competitions.competition_name == 'Champions League'])

    with open('../json/data/events/2302764.json') as f:
        data = json.load(f)
        df = pd.json_normalize(data, sep="_")
        df.head()

        first_half = df.loc[:1808, :]
        second_half = df.loc[1809:3551, :]

    home_team = 'AC Milan'
    away_team = 'Liverpool'

    select_team_name = team_select(st,home_team, away_team)

    pressure = first_half[df.type_name == 'Pressure']
    pressure = pressure[['team_name', 'player_name', 'location']]
    pressure = pressure[pressure.team_name == select_team_name]
    pressure['x'] = pressure.location.apply(lambda x: x[0])
    pressure['y'] = pressure.location.apply(lambda x: x[1])
    pressure = pressure.drop('location', axis=1)
    pressure.head()

    pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#22312b', line_color='#efefef')
    fig, axs = pitch.grid(figheight=10, title_height=0.08, endnote_space=0, axis=False, title_space=0, grid_height=0.82, endnote_height=0.05)
    fig.set_facecolor('#22312b')
    bin_statistic = pitch.bin_statistic(pressure.x, pressure.y, statistic='count', bins=(25, 25))
    bin_statistic['statistic'] = gaussian_filter(bin_statistic['statistic'], 1)
    pcm = pitch.heatmap(bin_statistic, ax=axs['pitch'], cmap='hot', edgecolors='#22312b')
    cbar = fig.colorbar(pcm, ax=axs['pitch'], shrink=0.6)
    cbar.outline.set_edgecolor('#efefef')
    cbar.ax.yaxis.set_tick_params(color='#efefef')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#efefef')
    axs['endnote'].text(0.8, 0.5, '[YOUR NAME]', color='#c7d5cc', va='center', ha='center', fontsize=10)
    axs['endnote'].text(0.4, 0.95, 'Attacking Direction', va='center', ha='center', color='#c7d5cc', fontsize=12)
    axs['endnote'].arrow(0.3, 0.6, 0.2, 0, head_width=0.2, head_length=0.025, ec='w', fc='w')
    axs['endnote'].set_xlim(0, 1)
    axs['endnote'].set_ylim(0, 1)
    axs['title'].text(0.5, 0.7, 'The Pressure\'s Heat Map from ' + select_team_name, color='#c7d5cc', va='center', ha='center', fontsize=30)
    axs['title'].text(0.5, 0.25, 'The Game\'s First Half', color='#c7d5cc', va='center', ha='center', fontsize=18)
    st.write(fig)

def team_select(st,home_team,away_team):
    select_box = [home_team,away_team]
    option = st.selectbox('조회하실 팀을 선택하여주세요.', select_box)
    return option