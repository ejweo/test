import streamlit as st
from lotto import Lotto
from soccer import *
from streamlit_option_menu import option_menu


st.title('재미삼아')

# 1. as sidebar menu
menu=['Home','로또','축구']
with st.sidebar:
    selected = option_menu("Main Menu", menu, icons=['house','list-columns-reverse','dribbble'], menu_icon="cast", default_index=0)

if selected==menu[1]:
    Lotto.lotto_main(st)
elif selected==menu[2]:
    soccer_main(st)

