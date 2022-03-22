import streamlit as st
from streamlit_option_menu import option_menu
from apps import home, geemap_script  # import your app modules here

st.set_page_config(page_title="Streamlit for Geospatial", layout="wide")

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com

apps = {
    "home": {"title": "Home", "icon": "house"},
    "geemap_script": {"title": "Chlorophyll-a", "icon": "map"},
}

titles = [app["title"] for app in apps.values()]
icons = [app["icon"] for app in apps.values()]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles.index(params["page"][0].lower()))
else:
    default_index = 0

with st.sidebar:
    selected = option_menu(
        "Main Menu",
        options=titles,
        icons=icons,
        menu_icon="cast",
        default_index=default_index,
    )

    st.sidebar.title("About")
    st.sidebar.info(
        """
        Aplikasi web ini dikelola ole Martanti Aji dengan dosen pembimbing Dr. Lalu Muhamad Jaelani S.T., M.Sc., PhD. 
        Url aplikasi web ini yaitu https://streamlit.geemap.org
        
        Anda dapat mengakses referensi kode : <https://github.com/martantiaji/klorofila.git>
        
    """
    )

for app in apps:
    if apps[app]["title"] == selected:
        eval(f"{app}.app()")
        break
