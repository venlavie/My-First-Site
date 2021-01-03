from django import forms
from django.conf import settings
import requests


class TeamForm(forms.Form):
    team = forms.CharField(max_length=100)

    def search(self):
        result = {}
        team = self.cleaned_data['team']
        endpoint = 'https://api.football-data.org/v2/teams/{team_id}/matches'
        url = endpoint.format(team_id=team)
        headers = { 'X-Auth-Token': 'd6b6f23c4af549b2890c6adda9c251d0' }
        response = requests.get(url, headers=headers)

        if response.status_code == 404:
            result['message'] = 'No entry found for "%s"' % team

        else:
            result = response.json()
            result['success'] = True


        return result