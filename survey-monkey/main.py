import api
import json


if __name__ == "__main__":

    # Read config file
    with open("config.json", encoding="utf-8") as data_file:
        config = json.load(data_file)

    CLIENT_ID = config['client_id']
    SECRET = config['secret']
    ACCESS_TOKEN = config['access_token']
    SURVEY_ID = config['survey_id']
    
    #Instantiate class with credentials
    api = api.SurveyResults(ACCESS_TOKEN)

    #Read responses from survey
    responses = api.get_survey_responses_new(SURVEY_ID)

    with open('responses.json', 'w') as f:
        json.dump(responses, f)

    #Read Survey Details    
    details = api.get_survey_details_new(SURVEY_ID)

    with open('details.json', 'w') as f:
        json.dump(details, f)

