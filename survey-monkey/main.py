import api
import data
import json


if __name__ == "__main__":

    # Read config file
    with open("config.json", encoding="utf-8") as data_file:
        config = json.load(data_file)

    CLIENT_ID = config['client_id']
    SECRET = config['secret']
    ACCESS_TOKEN = config['access_token']
    SURVEY_ID = config['survey_id']
    

    ###REMOVE THE COMMENTS FROM LINES ABOVE TO FETCH NEW ANSWERS:
    """
    ##Instantiate class with credentials
    api = api.SurveyResults(ACCESS_TOKEN)

    ##Read responses from survey
    responses = api.get_survey_responses_new(SURVEY_ID)

    with open('responses.json', 'w') as f:
        json.dump(responses, f)

    ##Read Survey Details    
    details = api.get_survey_details_new(SURVEY_ID)

    with open('details.json', 'w') as f:
        json.dump(details, f)
    """
    #################################################################

    with open("details.json", encoding="utf-8") as data_file:
        details = json.load(data_file)

    with open("responses.json", encoding="utf-8") as data_file:
        responses = json.load(data_file)    


    results = []
    for response in responses:
        results.append(data.flatten_data(response))


    df_result = data.to_dataframe(results)

    df_details = data.normalize(details, 'choices',['id_question', 'question'])
    
    df_questions = data.build_questions_df(df_details)
    df_answers = data.build_answers_id_df(df_details)

    counter = 0

    #map questions text
    """
    while counter < 99:
        field = 'answers_{}_question_id'.format(counter)
        try:
            df_result[field] = df_result[field].map(df_questions.set_index('id_question')['question'])
        except:
            counter = 99
        counter += 1
    """

    #Mapping Responses Texts
    counter = 0

    while counter < 99:
        counter2 = 0
        field = 'answers_{}_choices_{}_choice_id'.format(counter, counter2)
        try:
            df_result[field] = df_result[field].map(df_answers.set_index('id')['text'])
            while counter2 < 99:
                counter2 = counter2 + 1
                field = 'answers_{}_choices_{}_choice_id'.format(counter, counter2)
                try:
                    df_result[field] = df_result[field].map(df_answers.set_index('id')['text'])
                except:
                    counter2 = 99

        except:
            pass
        counter += 1


    rename = {'answers_0_choices_0_choice_id':'age', 'answers_1_choices_0_text':'name', 'answers_2_choices_0_choice_id':'like_1', 'answers_2_choices_1_choice_id':'like_2', 'answers_2_choices_2_choice_id':'like_3', 'answers_2_choices_3_choice_id':'like_4', 'answers_3_choices_0_choice_id':'food'}

    df_result = data.rename_column_df_new(df_result, rename)

    df_result = df_result[['survey_id','answer_id','response_status','date_created','name','age','like_1','like_2','like_3','food']]

    df_ages = data.read_total_answer(df_result,'age', 'survey_id')    

    df_ages.to_csv('ages.csv')

    df_result.to_csv('final.csv')

