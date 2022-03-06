import pandas as pd
from flatten_json import flatten
import json

def rename_column_df_new(df, rename):
   return df.rename(columns = rename)


def rename_column_df(df, new_column, old_column):
    try:
        return df.rename(columns = {old_column: new_column})
    except:
        return df

def read_total_answer(df, column, id):    
    return(df.value_counts(column).reset_index(name='counter'))



def build_answers_id_df(df):
    new_df = df.copy()
    new_df = new_df.drop(columns=['position', 'visible', 'id_question', 'question'])
    new_df = new_df.sort_values("id")
    new_df = new_df.drop_duplicates(subset='id')
    return new_df    

def build_questions_df(df):
    new_df = df.copy()
    new_df = new_df.drop(columns=['position', 'visible', 'text', 'id'])
    new_df = new_df.sort_values("id_question")
    new_df = new_df.drop_duplicates(subset='id_question')
    return new_df

def to_dataframe(array):
    return pd.DataFrame(array).drop(columns=['answers_1_choices_0_tag_data','answers_0_question_id','answers_1_question_id','answers_2_question_id','answers_3_question_id'])

def flatten_data(data):
    return flatten(data)


def normalize(json, record_path, meta):
    if len(meta) > 1:
        return pd.json_normalize(json, record_path=[record_path], meta=meta)
    else:
        return pd.json_normalize(json, record_path=[record_path])