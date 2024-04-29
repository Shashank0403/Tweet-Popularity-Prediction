import streamlit as st

from streamlit_option_menu import option_menu


import account, your
st.set_page_config(
        page_title="TwitPredict",
)


page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-color: rgba(255, 255, 255, 0.5); /* Adjust the alpha value (0-1) to control transparency */
    background-image: url("https://www.lifewire.com/thmb/55VlqROrh1QVHVbPhvDuSS7nHJw=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/Twitter-and-X-4c4103f6bc3c42e0b7197b60a50317ca.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}
</style>
"""


st.markdown(page_bg_img, unsafe_allow_html=True)


class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        # app = st.sidebar(
        with st.sidebar:        
            app = option_menu(
                menu_title='TwitPredict ',
                options=['Account','Predictor'],
                icons=['person-circle','chat-fill'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab21"},}
                
                )

        

        if app == "Account":
            account.app()    
        if app == 'Predictor':
            your.app()
   
             
          
             
    run()            
         
