import json
import base64
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

import streamlit.components.v1 as components
components.html("PASID")

import warnings
warnings.filterwarnings('ignore')

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




# st.set_page_config(
#         page_title="Mimicry for Pseudomonas Aeruginosa",
#         page_icon=Image.open("data/icon.png"),
#         layout="wide",
#         initial_sidebar_state="expanded"
# )


original_title = '<p style="font-family:sans-serif; color:#5E2750; font-size: 35px; font-weight:bold">PASID:  Pseudomonas Aeruginosa Structural Information Database</p>'
st.markdown(original_title, unsafe_allow_html=True)

biofilm_proteins = pd.read_csv('/data/biofilm_proteins_string_mapped.txt', sep='\t')
hmi_sub = pd.read_csv('/data/hmi_sub_with_identifiers.tsv', sep='\t')


selection = st.selectbox('Filter by', ("Filter by Pseudomonas Identifier", "Filter by Human Identifier"))

if selection == 'Filter by Pseudomonas Identifier':
    accession_selection = st.multiselect("Filter by Pseudomonas Identifier", biofilm_proteins.Entry)
    if len(accession_selection) > 0:
        biofilm_proteins_selected = biofilm_proteins[biofilm_proteins.Entry.isin(accession_selection)]
        if len(biofilm_proteins_selected) > 0:
            int_builder = GridOptionsBuilder.from_dataframe(biofilm_proteins_selected[["Entry", "Entry Name", "Protein names", "PDB"]])
            int_builder.configure_default_column(editable=False, filterable=True, cellStyle={'text-align': 'center'})
            int_builder.configure_column("Entry", header_name="UniProt Accession Number", editable=False, )
            int_builder.configure_column("Entry Name", header_name="UniProt ID")
            int_builder.configure_column("Protein names", header_name="Protein name")
            int_builder.configure_column("PDB", header_name="PDB")
            int_builder.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=10)
            int_builder.configure_selection(selection_mode='multiple',use_checkbox=True)
            st.markdown(f'<p class="main-font">Summary of selected protein. Select for a detailed view:</p>', unsafe_allow_html=True)
            gridoptions = int_builder.build()
            gridoptions["columnDefs"][0]["checkboxSelection"]=True
            gridoptions["columnDefs"][0]["headerCheckboxSelection"]=True
            with st.spinner('Loading data...'):
                int_return = AgGrid(biofilm_proteins_selected,
                                    width='100%',
                                    height=(len(biofilm_proteins_selected) + 4) * 35.2,
                                    theme='alpine',
                                    enable_enterprise_modules=False,
                                    gridOptions=gridoptions,
                                    fit_columns_on_grid_load=True,
                                    update_mode=GridUpdateMode.SELECTION_CHANGED, # or MODEL_CHANGED
                                    custom_css={".ag-header-cell-label": {"justify-content": "center;"}})

                if int_return["selected_rows"] is None:
                    pass
                else:
                    with st.spinner('Loading data...'):
                        selected_entry = int_return["selected_rows"]['Entry']
                        st.markdown(f'<p class="main-font">Structural mimicry table is shown for the selected Pseudomonas aeruginosa protein:</p>', unsafe_allow_html=True)
                        selected_df = hmi_sub[hmi_sub['PA Mimicking Protein Accession'].isin(selected_entry)]
                        selected_df = selected_df.reset_index(drop=True)
                        selected_df = selected_df.rename(columns ={'Human protein Name': 'Mimicked Human Protein Role', 'Microbial Protein Name': 'PA Mimicking Protein Role'})
                        int_builder = GridOptionsBuilder.from_dataframe(selected_df[["PA Mimicking Protein Accession", "PA Mimicking Protein Name", "Microbe Protein PDB", "PA Mimicking Protein Role",
                                                                                   "Mimicked Human Protein Accession", "Mimicked Human Protein Name", "Mimicked Human Protein Role", "Human protein PDB",
                                                                                   "Template interface", "Mimicked/disrupted human PPI", "I_SC for modeled HMI", "I_SC for template PPI", "# of aligned residues ",
                                                                                   "Length of template interface", "%Match", "Probability of being a biological interface", "Score1", "Score2", "Score3"]])
                        int_builder.configure_default_column(editable=False, filterable=True, cellStyle={'text-align': 'center'})
                        int_builder.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=10)
                        int_builder.configure_selection(selection_mode='multiple', use_checkbox=True)
                        gridoptions = int_builder.build()
                        gridoptions["columnDefs"][0]["checkboxSelection"]=True
                        gridoptions["columnDefs"][0]["headerCheckboxSelection"]=True
                        selected_df = selected_df[["PA Mimicking Protein Accession", "PA Mimicking Protein Name", "Microbe Protein PDB", "PA Mimicking Protein Role",
                                                                                   "Mimicked Human Protein Accession", "Mimicked Human Protein Name", "Mimicked Human Protein Role", "Human protein PDB",
                                                                                   "Template interface", "Mimicked/disrupted human PPI", "I_SC for modeled HMI", "I_SC for template PPI", "# of aligned residues ",
                                                                                   "Length of template interface", "%Match", "Probability of being a biological interface", "Score1", "Score2", "Score3"]]
                        with st.spinner('Loading data...'):
                            int_return = AgGrid(selected_df,
                                            width='100%',
                                            height=(len(selected_df) + 4) * 40 + 6,
                                            theme='alpine',
                                            enable_enterprise_modules=False,
                                            gridOptions=gridoptions,
                                            fit_columns_on_grid_load=False,
                                            update_mode=GridUpdateMode.SELECTION_CHANGED, # or MODEL_CHANGED
                                            custom_css={".ag-header-cell-label": {"justify-content": "center"}})
                        # This is needed to download only selected
                        selected_row = int_return["selected_rows"]
                        selected_df = pd.DataFrame(selected_row, columns=selected_df.columns)

st.markdown(f'<p class="main-font"> Select from the detailed interface information table to download: </p>',
            unsafe_allow_html=True)

with st.form("my_form", clear_on_submit=False):
    st.text_input("Enter filename", key="filename")
    submit = st.form_submit_button("Download", on_click=download_df)

new_title = '<p style="font-family: sans-serif; text-align: center; color:#77216F; font-size: 16px;">For more information about how to use this website, please visit User Guide Page in the navigation panel.</p>'
st.markdown(new_title, unsafe_allow_html=True)

