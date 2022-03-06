import requests
import json


class ApiCall(object):
    def __init__(self, access_token):
        self.host = "https://api.surveymonkey.net/v3/"
        self.client = requests.session()
        self.client.headers = {
            "Authorization": "Bearer %s" % access_token,
            "Content-Type": "application/json"
        }

    def get_data(self, url):
        results = self.client.get(url)
        return results


class SurveyResults(ApiCall):
    def __init__(self, access_token):
        super().__init__(access_token)

    def get_survey_details_new(self, survey_id):
        """ Make a call to get survey details """
        url = self.host + "surveys/%s/details" % (survey_id)
        response = self.client.get(url).json()
        results = []

        # Loop through pages to get question details
        pages = response['pages']        
        for page in pages:
            title = ''
            results = []
            choices = []

            questions = page['questions']


            for question in questions:

                headings = question['headings']

                for heading in headings:
                    title = heading['heading']
                

                if 'answers' in question:
                    choices = question['answers']['choices']
                    choices_result = [{k: v for k, v in d.items() if k != 'quiz_options'} 
                         for d in choices]                    
                else:
                    
                    choices_result = [{'position':1}]

                answer = {'id_question':question['id'], 'question': title, 'choices': choices_result}

                results.append(answer)
        
        return results        


    def get_survey_responses_new(self, survey_id):
        """ Make calls to loop through all survey responses """

        url = self.host + 'surveys/%s/responses/bulk/?per_page=100' % (survey_id)
        response = self.client.get(url).json()
        results = []
        answers = response['data']

        for answer in answers:
            survey_id = answer['survey_id']
            answer_id = answer['id']
            response_status = answer['response_status']
            date_created = answer['date_created']
            answers = []

            for page in answer['pages']:
                for question in page['questions']:                    
                    question_id = question['id']
                    choices = question['answers']
                    answers.append({'question_id':question_id,'choices':choices})

            result = {'survey_id':survey_id, 'answer_id':answer_id, 'response_status':response_status, 'date_created':date_created, 'answers':answers}
            results.append(result)

        return results

        


