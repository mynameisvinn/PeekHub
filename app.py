import hub
from hub import transform
import uuid
import streamlit as st
import numpy as np
from twilio.rest import Client 

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



st.title("PeekHub")
st.write("A no-fuss way to downsample large, out-of-core datasets while preserving its distribution. That means downsampling your dataset of (:dog: :dog: :dog: :dog: :cat: :cat:) by 50% results in (:dog: :dog: :cat:). \n We shrink datasets so you don't have to.")

options = [
    'mnist', 
    'cifar10_train', 
    'cifar100_train', 
    'omniglot_test',
    'objectron_camera',
    'lm1b',
    'twitter_airline',
    'CoLA',
    'dota',
    'kitti_train',
    'deep_weeds_train',
    'voc_2012_train',
    'food101_train',
    'cars196_test',
    'eurosat_train',
    'coil100_train',
    'the300w_lp_train',
    'caltech_birds2010_train',
    'beans_train',
    'stl10_unlabelled',
    'dtd_train',
    'malaria_train']

datasets = st.multiselect("Dataset", options)

if datasets:
    subset = st.slider('Fraction to keep', min_value=0.0, max_value=1.0, value=0.0, step=0.05)

    if subset != 0:
        selected_dataset = datasets[0]
        st.write(f'Slicing {subset} of {selected_dataset}')
        
        tag = "mynameisvinn/{}-{}-{}".format(selected_dataset, uuid.uuid1(), subset)
        src = f'activeloop/{selected_dataset}'

        if peek(src=src, dst=tag, k=subset):
            st.write("Fetch dataset from Hub")
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