import uuid

import hub
from hub import transform
import streamlit as st
import numpy as np

from utils import _generate_dict, _peek
from config import DATASETS


st.title("PeekHub")
st.write("A no-fuss way to downsample large, out-of-core datasets while preserving its distribution. That means downsampling your dataset of (:dog: :dog: :dog: :dog: :cat: :cat:) by 50% results in (:dog: :dog: :cat:). \n We shrink datasets so you don't have to.")

datasets = st.multiselect("Dataset", DATASETS)
if datasets:
    subset = st.slider('Fraction to keep', min_value=0.0, max_value=1.0, value=0.0, step=0.2)

    if subset != 0:
        selected_dataset = datasets[0]
        st.write(f'Slicing {subset} of {selected_dataset}')
        
        tag = "mynameisvinn/{}-{}-{}".format(selected_dataset, uuid.uuid1(), subset)
        src = f'activeloop/{selected_dataset}'

        if _peek(src=src, dst=tag, k=subset):
            st.write(f"Fetching {selected_dataset} from Hub")
            body = f"""import hub \nds = hub.load('{tag}')""".format(tag)
            st.code(body, language='python')
        
            ds = hub.load(f'{src}')
            keys = ds.schema.dict_
            code = ""

            for k in keys:
                snippet = "{}s = ds['{}'].compute()".format(k, k)
                code += snippet
                code += '\n'
            st.code(code, language='python')

        else:
            st.write("Slicing failed, sorry!")
