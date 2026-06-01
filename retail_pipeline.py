#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

file = "USECASE - Data Engineering.xlsx"

retail1 = pd.read_excel(file,sheet_name="retail_data1")
retail2 = pd.read_excel(file,sheet_name="retail_data2")
products = pd.read_excel(file,sheet_name="product_details")


# In[2]:


retail = pd.concat([retail1, retail2])


# In[3]:


category_map = {
    "ELEC":"Electronics",
    "electronics":"Electronics",

    "FURN":"Furniture",
    "furniture":"Furniture",

    "HOME":"Home Appliances",
    "home appliances":"Home Appliances",

    "CLOTH":"Clothing",
    "clothing":"Clothing"
}

retail["category"] = retail["category"].replace(category_map)


# In[ ]:





# In[4]:


retail["product_name"] = (
    retail["product_name"]
    .str.strip()
    .str.title()
)


# In[5]:


retail = retail.merge(
    products,
    on="product_id",
    how="left",
    suffixes=("", "_master")
)


# In[6]:


retail["price"] = retail["price"].fillna(
    retail["price_master"]
)


# In[7]:


retail = retail[
    retail["quantity"] > 0
]


# In[8]:


retail["transaction_date"] = pd.to_datetime(
    retail["transaction_date"],
    errors="coerce"
)


# In[9]:


import hashlib

retail["email_masked"] = retail["email"].apply(
    lambda x:
    hashlib.sha256(
        str(x).encode()
    ).hexdigest()
)


# In[10]:


retail["phone_masked"] = retail["phone"].astype(str).apply(
    lambda x:
    x[:2] + "******" + x[-2:]
)


# In[11]:


retail["revenue"] = (
    retail["price"]
    * retail["quantity"]
    * (1-retail["discount"])
)


# In[12]:


retail.to_csv(
    "cleaned_retail.csv",
    index=False
)


# In[ ]:




