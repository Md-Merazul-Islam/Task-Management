from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.views.decorators.csrf import csrf_exempt


class GeminiAPIView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        api_key = 'AIzaSyACFXo4-dpmCEs0AWeD1RSZ6lfxea3jue8'
        headers = {'Content-Type': 'application/json'}

        user_text = request.data.get("text", "Explain how AI works")

        data = {
            "contents": [
                {"parts": [{"text": user_text}]}
            ]
        }

        response = requests.post(
            api_url, headers=headers, json=data, params={'key': api_key})

        if response.status_code == 200:
            return Response({
                "user_input": user_text,
                "generated_content": response.json(),
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "Failed to fetch content from Gemini API",
                "details": response.text,
                "user_input": user_text
            }, status=status.HTTP_400_BAD_REQUEST)



from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.views.decorators.csrf import csrf_exempt


class ProjectOptimizationAPIView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = request.data
        prompt = f"""
        The project name is '{data['project_name']}'. The objective is to {data['objective']}. 
        The project has the following phases: 
        {', '.join([f"{phase['name']} from {phase['start_date']} to {phase['end_date']}" for phase in data['phases']])}.
        The resources include {data['resources']['developers']} developers, {data['resources']['designers']} designers,
        a budget of ${data['resources']['budget']}, and external testing vendor: {data['resources']['external_testing_vendor']} .
        The challenges include {', '.join(data['challenges'])}.
        {data['developer_prompt']}
        """
        print(prompt)
        print("--------------------------------------------------------------------------------------------------------")

        # Gemini API URL
        api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        api_key = 'AIzaSyACFXo4-dpmCEs0AWeD1RSZ6lfxea3jue8'
        headers = {'Content-Type': 'application/json'}
        
        data = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }

        try:
            # Send request to Gemini API
            response = requests.post(api_url, headers=headers, json=data, params={'key': api_key})
            if response.status_code == 200:
                return Response({
                    "generated_content": response.json(),
                    "user_prompt": prompt
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "error": "Failed to fetch content from Gemini",
                    "details": response.text,
                    "user_prompt": prompt
                }, status=status.HTTP_400_BAD_REQUEST)

        except requests.exceptions.RequestException as e:
            return Response({
                "error": "Error while making request to Gemini",
                "details": str(e),
                "user_prompt": prompt
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
