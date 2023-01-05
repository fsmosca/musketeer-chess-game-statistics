from deta import Deta  # Import Deta
import pandas as pd
import streamlit as st


detapro = Deta(st.secrets["deta_base_key"])
db = detapro.Base("musketeerchessdb")

def get_all():
    res = db.fetch()
    all_items = res.items
    df = pd.DataFrame(all_items)
    return df
