import requests


class ServiceLoader(object):

    def __init__(self, api_url, access_token):
        self.api_url = api_url
        self.access_token = access_token
        if self.access_token is None:
            print('Token must be supplied in DM_ADMIN_FRONTEND_API_AUTH_TOKEN')
            raise Exception("DM_ADMIN_FRONTEND_API_AUTH_TOKEN token not set")
        if self.api_url is None:
            print('API URL must be supplied in DM_API_URL')
            raise Exception("DM_API_URL is not set")

    def get(self, service_id):
        response = requests.get(
            self.api_url + "/services/" + service_id,
            headers={
                "authorization": "Bearer {}".format(self.access_token)
            }
        )

        return response.json()["services"]

    def set(self, data, key, value):
        data[key] = value
        return data

    def post(self, data):
        print(data)  # This would be an update call to the API
