import streamlit as st
from streamlit_d3graph import d3graph, vec2adjmat

from langchain_community.document_loaders import PyPDFLoader

from docparser import split_documents
from prompts import construct_prompt
from ontology import get_ontology
from graph_merger import join_graphs

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

BGCOLOR="rgb(38, 39, 48)"

@st.cache_data
def init_graph():
    # Initialize
    d3 = d3graph()
    # Load example
    source = ["CollegeCourtyardApartments&RaiderHousing"] * 7
    target = ["Knowledge", "28&30GardenLaneNicevilleFL32578", "62Units", "OkaloosaWaltonCommunityCollegeFoundationInc", "EquiValueAppraisalLLC", "5000000USD", "December132019"]
    label = ["is a concept of", "located at", "comprises", "owned by", "appraised by", "valued at", "appraisal date"]
    weight = [0.1, 1, 1, 1, 0.9, 1, 0.9]
    adjmat = vec2adjmat(source=source, target=target, weight=weight)

    return d3, label, adjmat

#@st.cache_data
def graph(d3, label, adjmat):
    d3.graph(adjmat)
    d3.set_edge_properties(edge_distance=100, label=label)
    return d3

def generate_graph():
    d3, label, adjmat = init_graph()
    d3 = graph(d3=d3, label=label, adjmat=adjmat)
    d3.show(show_slider=False)

def connect_to_bedrock():
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    return llm

def main():
    llm = connect_to_bedrock()

    st.set_page_config(layout="wide")

    col1, col2 = st.columns([0.4, 0.6])

    with col1:
        file_link = st.text_input(
            label="Document Link", 
            key="file_link", 
            value="https://raw.githubusercontent.com/skarlekar/graph-visualizer/1927533f5b79fd1fd529944d77462553e7fe9bde/content/Appraisal-Report.pdf"
        )

        ontology = st.text_area(
            label="Ontology TTL",
            height=400,
            value=get_ontology(),
        )

    with col2:
        if st.button("Generate Graph"):
            if file_link and ontology:
                loader = PyPDFLoader(file_link)
                #pages = loader.load_and_split()
                doc = loader.load()
                texts = split_documents(chunk_size=1000, document=doc)

                tab1, tab2, tab3 = st.tabs(["Graph 1", "Graph 2", "Merged Graph"])

                with tab1:
                    prompt = construct_prompt(ontology=ontology, text=texts[0].page_content)
                    response = llm.invoke(input=prompt)
                    st.text(f"""{response.content}""")
                
                with tab2:
                    prompt2 = construct_prompt(ontology=ontology, text=texts[1].page_content)
                    response2 = llm.invoke(input=prompt2)
                    st.divider()
                    st.text(f"""{response2.content}""")
                
                with tab3:
                    st.divider()
                    joined_graph = join_graphs(graph1=response.content, graph2=response2.content, llm=llm)
                    st.text(f"""{joined_graph}""")
            else:
                st.error('Document or ontology is missing', icon="🚨")

if __name__ == '__main__':
    main()
