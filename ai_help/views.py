# import requests
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.conf import settings
# import logging
# from django.views.decorators.csrf import csrf_exempt
# # Configure logging
# logger = logging.getLogger(__name__)

# class GeminiAPIView(APIView):
#     @csrf_exempt
#     def post(self, request, *args, **kwargs):
#         # Construct the Gemini API URL
#         api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
#         api_key = settings.GOOGLE_API_KEY

#         if not api_key:
#             logger.error("API key is missing in settings.")
#             return Response({"error": "API key is not configured in settings."}, status=status.HTTP_400_BAD_REQUEST)

#         # Set the headers for the request
#         headers = {
#             'Content-Type': 'application/json',
#         }

#         # Extract the text from the request, providing a default if not found
#         text_query = request.data.get("text", "Explain how AI works")

#         # Define the payload data
#         data = {
#             "contents": [
#                 {
#                     "parts": [
#                         {"text": text_query}
#                     ]
#                 }
#             ]
#         }

#         # Add the API key as a query parameter
#         params = {
#             "key": api_key
#         }

#         try:
#             # Use a session to optimize HTTP connection reuse
#             with requests.Session() as session:
#                 response = session.post(api_url, headers=headers, json=data, params=params)
#             if response.status_code == 200:
#                 return Response(response.json(), status=status.HTTP_200_OK)

#             # If not, log the error and return a message
#             logger.error(f"Gemini API failed with status {response.status_code}: {response.text}")
#             return Response({
#                 "error": "Failed to fetch content from Gemini API",
#                 "details": response.text
#             }, status=status.HTTP_400_BAD_REQUEST)

#         except requests.exceptions.RequestException as e:
#             # Catch any request exceptions and log the error
#             logger.error(f"Error during API request: {e}")
#             return Response({
#                 "error": "An error occurred while making the request to Gemini API",
#                 "details": str(e)
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.views.decorators.csrf import csrf_exempt


class GeminiAPIView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        # Your API interaction code
        api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        api_key = 'AIzaSyACFXo4-dpmCEs0AWeD1RSZ6lfxea3jue8'  # Or load it from settings
        headers = {'Content-Type': 'application/json'}

        # Get the input text from the request (default if empty is "Explain how AI works")
        user_text = request.data.get("text", "Explain how AI works")

        data = {
            "contents": [
                {"parts": [{"text": user_text}]}
            ]
        }

        # Make the request to the Gemini API
        response = requests.post(
            api_url, headers=headers, json=data, params={'key': api_key})

        if response.status_code == 200:
            # Return the response from Gemini API along with the original input
            return Response({
                "user_input": user_text,
                # Return the full response from Gemini API
                "generated_content": response.json(),
            }, status=status.HTTP_200_OK)
        else:
            # If an error occurs, return the error message and details
            return Response({
                "error": "Failed to fetch content from Gemini API",
                "details": response.text,
                "user_input": user_text  # Include the input text to show it to the user
            }, status=status.HTTP_400_BAD_REQUEST)
