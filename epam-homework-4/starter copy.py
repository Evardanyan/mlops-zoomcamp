#!/usr/bin/env python
# coding: utf-8

# In[6]:


get_ipython().system('pip freeze | grep scikit-learn')


# In[8]:


import pickle
import pandas as pd


# In[7]:


get_ipython().system('python -V')


# In[12]:


get_ipython().system('pip install pyarrow')


# In[17]:


with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)


# In[18]:


categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


# In[19]:


df = read_data('https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet')


# In[20]:


df


# In[23]:


import numpy as np
dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)
print("Standard deviation:", np.std(y_pred))


# **Standard deviation is 6.247488852238703**

# In[25]:


year = 2023
month = 3


# In[26]:


df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')


# In[27]:


df


# In[29]:


df_result = pd.DataFrame({
    'ride_id': df['ride_id'],
    'predicted_duration': y_pred
})


# In[31]:


output_file = 'predictions_2023_03.parquet'


# In[32]:


df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)


# In[33]:


import os
file_size_bytes = os.path.getsize(output_file)
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"File size: {file_size_mb:.2f} MB")


# **File size is 65.46 MB**

# In[ ]:




