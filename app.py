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

datasets = st.multiselect("Dataset", ['activeloop/mnist', 'activeloop/cifar10_train'])

if datasets:    
    tag = "mynameisvinn/{}".format(uuid.uuid1())
    peek(src=datasets[0], dst=tag, k=0.02)
    
    st.write("Code snippet")
    body = f"""
        import hub            
        ds = hub.load('{tag}')
        """.format(tag)
    st.code(body, language='python')
