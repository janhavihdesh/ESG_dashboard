import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import matplotlib
import numpy as np


import metadata_parser
warnings.filterwarnings('ignore')


st.set_page_config(page_title="ESG Data EDA", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: ESG Data EDA")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding="ISO-8859-1")
else:
    os.chdir(r"C:\Users\vaish\Desktop\hack\Data")
    df = pd.read_csv("data_as_csv.csv", encoding="ISO-8859-1")
# Define the columns for this dataset
columns = [
    "SourceCommonName",
    "URL",
    "E",
    "S",
    "G",
    "Organization",
    "Tone",
    "PositiveTone",
    "NegativeTone",
    "Polarity",
    "ActivityDensity",
    "SelfDensity",
    "WordCount"
]

col1, col2 = st.columns((2))


# Create filters for your dataset
with st.sidebar.expander("Filter by Organization"):
    selected_organizations = st.sidebar.multiselect("Select Organization", df["Organization"].unique())
    if selected_organizations:
        df = df[df["Organization"].isin(selected_organizations)]

#filer for publisher
with st.sidebar.expander("Filter by Publisher"):
    selected_SourceCommonName = st.sidebar.multiselect("Select publisher", df["SourceCommonName"].unique())
    if selected_SourceCommonName:
        df = df[df["SourceCommonName"].isin(selected_SourceCommonName)]
        
# Create a scatter plot to visualize a relationship between two numerical columns
x_col = st.selectbox("Select the X-axis column", df.select_dtypes(include=[np.number]).columns)
y_col = st.selectbox("Select the Y-axis column", df.select_dtypes(include=[np.number]).columns)
fig = px.scatter(df, x=x_col, y=y_col, title=f'Scatter Plot of {x_col} vs. {y_col}')
st.plotly_chart(fig)


#filer for pconnection
st.sidebar.title("Filter Options")
date_place = st.sidebar.empty()
esg_categories = st.sidebar.multiselect("Select News Categories",
                                            ["E", "S", "G"], ["E", "S", "G"])
pub = st.sidebar.empty()
num_neighbors = st.sidebar.slider("Number of Connections", 1, 20, value=8)



# Example: Data Table
with st.expander("View Data"):
    st.write(df.iloc[:500, :].style.background_gradient(cmap="Oranges"))

# Download the original dataset
csv = df.to_csv(index=False).encode('utf-8')
st.download_button('Download Data', data=csv, file_name="ESG_Data.csv", mime="text/csv")
