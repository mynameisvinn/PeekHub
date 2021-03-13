import hub
from hub import transform
import uuid
import streamlit as st
import numpy as np

def _generate_dict(x, keys):
    d = {}
    for key in keys:
        key = key.split('/')[-1]
        d[key] = x[key]
    return d
    
    
def peek(src, dst, k):
    ds = hub.load(src)
    ds3 = ds.filter(lambda x: np.random.uniform() > (1-k))  # creates datasetview
    
    @transform(schema=ds3.schema)
    def load_transform1(sample, stuff):
        di = _generate_dict(sample, stuff)
        return di
    
    ds4 = load_transform1(ds3, stuff=list(ds3.keys))
    ds5 = ds4.store(dst)
    return True



st.title("Peek")
st.write('A no-fuss way to downsample datasets.')

options = ['activeloop/mnist', 'activeloop/cifar10_train', "activeloop/cifar100_train", "activeloop/omniglot_test"]
datasets = st.multiselect("Dataset", options)

if datasets:
    subset = st.slider('Keep %', min_value=0.0, max_value=1.0, value=0.0, step=0.05)
    if subset != 0:
        st.write('Slicing', subset)
        tag = "mynameisvinn/{}".format(uuid.uuid1())
        peek(src=datasets[0], dst=tag, k=subset)
        
        st.write("Code snippet")
        body = f"""
            import hub            
            ds = hub.load('{tag}')
            """.format(tag)
        st.code(body, language='python')
