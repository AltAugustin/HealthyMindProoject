
import os 
import pandas  as pd
import re
import numpy as np
import re
from transformers import TFBertModel,  BertConfig, BertTokenizerFast
from tensorflow.keras.layers import Input, Dropout, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.initializers import TruncatedNormal
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras.metrics import CategoricalAccuracy

def clean_text(text):
    REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
    BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
    text = text.lower() 
    text = REPLACE_BY_SPACE_RE.sub(' ', text) 
    text = BAD_SYMBOLS_RE.sub('', text)  
    return text
    
def main_function(file_txt):
    text_line = []
    for m in file_txt.split("\n"):
      if len(m)>50:
        text_line.append([m])
    df = pd.DataFrame(text_line,columns=["text"])
    df['text'] = df['text'].apply(clean_text)

    # Name of the BERT model to use
    model_name = 'bert-base-uncased'
    # Max length of tokens
    max_length = 50
    # Load transformers config and set output_hidden_states to False
    config = BertConfig.from_pretrained(model_name)
    config.output_hidden_states = False
    # Load BERT tokenizer
    tokenizer = BertTokenizerFast.from_pretrained(pretrained_model_name_or_path = model_name, config = config)
    # Load the Transformers BERT model
    transformer_model = TFBertModel.from_pretrained(model_name, config = config)

    # customizing the model to fit our project. We are using bert as back layers and in front we are 
    # adding dense layer which will classify the text in 3 classes

    bert = transformer_model.layers[0]
    # Build your model input
    input_ids = Input(shape=(max_length), name='input_ids', dtype='int32')
    inputs = {'input_ids': input_ids}
    # Load the Transformers BERT model as a layer in a Keras model
    bert_model = bert(inputs)[1]
    dropout = Dropout(0.2)
    pooled_output = dropout(bert_model, training=False)
    # Then build your model output
    issue = Dense(units=75)(pooled_output)
    issue = Dropout(0.5)(issue)
    product = Dense(units=3)(issue)
    outputs = { 'product': product}
    # And combine it all in a model object
    model = Model(inputs=inputs, outputs=outputs, name='BERT_MultiLabel_MultiClass')
    


    optimizer = Adam(
        learning_rate=5e-05,
        epsilon=1e-08,
        decay=0.01,
        clipnorm=1.0)
    # Set loss and metrics

    loss = {'product': CategoricalCrossentropy(from_logits = True)}
    metric = {'product': CategoricalAccuracy('accuracy')}
    # Compile the model
    model.compile(
        optimizer = optimizer,
        loss = loss, 
        metrics = metric)

    test_x1 = tokenizer(
        text=df['text'].to_list(), 
        add_special_tokens=True,
        max_length=max_length,
        truncation=True,
        padding=True, 
        return_tensors='tf',
        return_token_type_ids = False,
        return_attention_mask = False,
        verbose = True)
    model_test = model.predict(
        x={'input_ids': test_x1['input_ids']}
    )

    a = 0
    b = 0
    c = 0
    for d in model_test["product"]:
      a = a + max(d[0],0)
      b = b + max(d[1],0)
      c = c + max(d[2],0)

    total = a+b+c
    clusterA = a/total*100
    clusterB = b/total*100
    clusterC = c/total*100
    final_return = [clusterA,clusterB,clusterC]
    return final_return   
    
   



