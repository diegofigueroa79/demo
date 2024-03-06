import streamlit as st
from streamlit_d3graph import d3graph, vec2adjmat


d3 = d3graph()

source = ["CollegeCourtyardApartments&RaiderHousing"] * 7
target = ["Knowledge", "28&30GardenLaneNicevilleFL32578", "62Units", "OkaloosaWaltonCommunityCollegeFoundationInc", "EquiValueAppraisalLLC", "5000000USD", "December132019"]
label = ["is a concept of", "located at", "comprises", "owned by", "appraised by", "valued at", "appraisal date"]
weight = [0.1, 1, 1, 1, 0.9, 1, 0.9]

adjmat = vec2adjmat(source=source, target=target, weight=weight)

d3.graph(adjmat)
d3.set_edge_properties(edge_distance=100, label=label)
d3.show(show_slider=False)
