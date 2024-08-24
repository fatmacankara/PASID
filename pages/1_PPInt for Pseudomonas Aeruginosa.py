
import streamlit as st
import pandas as pd
import numpy as np
import base64
import json
import warnings
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode

import streamlit.components.v1 as components

def download_button(object_to_download, download_filename):
    """
    Generates a link to download the given object_to_download.
    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    Returns:
    -------
    (str): the anchor tag to download object_to_download
    """
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # Try JSON encode for everything else
    else:
        object_to_download = json.dumps(object_to_download)
    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    dl_link = f"""
            <html>
            <head>
            <title>Start Auto Download file</title>
            <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
            <script>
            $('<a href="data:text/csv;base64,{b64}" download="{download_filename}">')[0].click()
            </script>
            </head>
            </html>
            """
    return dl_link


def download_df():
   st._main._html(
        download_button(selected_df, st.session_state.filename),
        height=0,
    )



warnings.filterwarnings('ignore')

# st.set_page_config(
#     page_title="PASID",
#     page_icon="🧬",
#     layout="centered",
#     initial_sidebar_state="expanded")

original_title = '<p style="font-family:sans-serif; color:#5E2750; font-size: 35px; font-weight:bold">PASID:  Pseudomonas Aeruginosa Structural Information Database</p>'
st.markdown(original_title, unsafe_allow_html=True)
st.markdown(""" 
 <style>
  .main-font
  { 
  font-family:sans-serif; font-size:16px;text-align: justify
  }
</style>""", unsafe_allow_html=True)
# Read Data
display_df = pd.read_csv('data/ppint_pa_filtered_streamlit.txt', sep='\t')
display_df.drop(columns = ['int_id', 'unit_id', 'biounit', 'pdb_id'], inplace=True)

# Fix Table
selection = st.selectbox('Filter by', ("Filter by PDB ID", "Filter by UniProt ID"))
if selection == 'Filter by PDB ID':
    ligand_selection = st.multiselect("PDB ID", list(set(display_df['pdbID'])))
    if len(ligand_selection) > 0:
        display_df = display_df[display_df['pdbID'].isin(ligand_selection)]
    else:
        display_df = pd.DataFrame(columns  = display_df.columns)
if len(display_df) > 0:
    int_builder = GridOptionsBuilder.from_dataframe(display_df[['pdbID',  'chain_1','chain_2',
                                                                'num_contacting_1', 'num_contacting_2', 'num_nearby_1',
                                                                'num_nearby_2', 'sum_contacting', 'sum_nearby']])
    int_builder.configure_default_column(editable=False, filterable=True, cellStyle={'text-align': 'center'})
    int_builder.configure_column("pdbID", header_name="PDB ID")
    int_builder.configure_column("chain_1", header_name="Chain 1")
    int_builder.configure_column("chain_2", header_name="Chain 2")
    # int_builder.configure_column('contacting', header_name="Contacting Interface Residues (CIR)")
    # int_builder.configure_column("nearby", header_name="Nearby Interface Residues (NIR)")
    int_builder.configure_column("num_contacting_1", header_name="# CIR of First Partner")
    int_builder.configure_column("num_contacting_2", header_name="# CIR of Second Partner")
    int_builder.configure_column("num_nearby_1", header_name="# NIR of First Partner")
    int_builder.configure_column("num_nearby_2", header_name="# NIR of Second Partner")
    int_builder.configure_column("sum_contacting", header_name="# Sum CIR")
    int_builder.configure_column("sum_nearby", header_name="# Sum NIR")

    int_builder.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=50)
    int_builder.configure_selection(selection_mode='multiple', use_checkbox=True)
    st.markdown(f'<p class="main-font">List of selected ligands:</p>', unsafe_allow_html=True)

    gridoptions = int_builder.build()
    gridoptions["columnDefs"][0]["checkboxSelection"] = True
    gridoptions["columnDefs"][0]["headerCheckboxSelection"] = True
    from st_aggrid import AgGrid
    with st.spinner('Loading data...'):
        st.write('dn')
        int_return = AgGrid(display_df,
                            width='100%',
                            height=(len(display_df) + 4) * 40,
                            theme='alpine',
                            enable_enterprise_modules=False,
                            gridOptions=gridoptions,
                            fit_columns_on_grid_load=True,
                            update_mode=GridUpdateMode.SELECTION_CHANGED, # or MODEL_CHANGED
                            custom_css={".ag-header-cell-label": {"justify-content": "center;"}})

        st.write('aa')
        if int_return["selected_rows"] is None:
            pass
        else:
            with st.spinner('Loading data...'):
                st.markdown(f'<p class="main-font">Detailed view of interface residues: </p>', unsafe_allow_html=True)
                selected_row = int_return["selected_rows"]
                selected_df = pd.DataFrame(int_return["selected_rows"], columns=display_df.columns)
                selected_df['interface_id'] = selected_df['pdbID'] + '_' + selected_df['chain_1'] + '_' + selected_df['chain_2']
                selected_df = selected_df[['interface_id', 'contacting_residues', 'nearby_residues']]
                int_builder = GridOptionsBuilder.from_dataframe(selected_df)
                int_builder.configure_default_column(editable=False, filterable=True, cellStyle={'text-align': 'center'})
                int_builder.configure_column("interface_id", header_name="Interface ID")
                int_builder.configure_column("contacting_residues", header_name="Contacting Interface Residues")
                int_builder.configure_column("nearby_residues", header_name="Nearby Interface Residues")
                int_builder.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=10)
                int_builder.configure_selection(selection_mode='multiple', use_checkbox=True)
                gridoptions = int_builder.build()
                gridoptions["columnDefs"][0]["checkboxSelection"] = True
                gridoptions["columnDefs"][0]["headerCheckboxSelection"] = True
                with st.spinner('Loading data...'):
                    int_return = AgGrid(selected_df,
                                    width='100%',
                                    height=(len(selected_df) + 4) * 40,
                                    theme='alpine',
                                    enable_enterprise_modules=False,
                                    gridOptions=gridoptions,
                                    fit_columns_on_grid_load=False,
                                    update_mode=GridUpdateMode.SELECTION_CHANGED, # or MODEL_CHANGED
                                    custom_css={".ag-header-cell-label": {"justify-content": "center"}})
                # This is needed to download only selected
                selected_row = int_return["selected_rows"]
                selected_df = pd.DataFrame(selected_row, columns=selected_df.columns)

st.markdown(f'<p class="main-font"> Select from the calculated property table to download: </p>',
            unsafe_allow_html=True)

with st.form("my_form", clear_on_submit=False):
    st.text_input("Enter filename", key="filename")
    submit = st.form_submit_button("Download", on_click=download_df)

new_title = '<p style="font-family: sans-serif; text-align: center; color:#77216F; font-size: 16px;">For more information about how to use this website, please visit User Guide Page in the navigation panel.</p>'
st.markdown(new_title, unsafe_allow_html=True)
