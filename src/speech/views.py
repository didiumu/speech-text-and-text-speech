import os
import tempfile
import json
from django.http import FileResponse, JsonResponse
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import requests
from TTS.api import TTS

# Initialize the Coqui TTS model
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

# Endpoint for text-to-speech conversion (API)
@csrf_exempt
@require_http_methods(["POST"])
def text_to_speech_api(request):
    try:
        # Check if the request body is present and properly decoded
        if hasattr(request, 'body'):
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request

        text = data.get('text')
        if not text:
            return JsonResponse({"error": "No text provided"}, status=400)

        # Optional parameters for model selection, speaker, and speed
        model_name = data.get('model', "tts_models/en/ljspeech/tacotron2-DDC")
        speaker = data.get('speaker', None)
        speed = float(data.get('speed', 1.0))

        # Handling multilingual models
        is_multi_lingual = "multilingual" in model_name or "multi-dataset" in model_name
        language = data.get('language', 'en') if is_multi_lingual else None

        # Using Hugging Face API for additional services (e.g., text classification)
        hf_token = settings.HF_ACCESS_TOKEN  # Retrieve Hugging Face token from settings

        if hf_token:
            hf_api_url = "https://api-inference.huggingface.co/models/your_model_name"
            headers = {
                "Authorization": f"Bearer {hf_token}",
                "Content-Type": "application/json"
            }
            # Sending the text to Hugging Face API for processing
            hf_response = requests.post(hf_api_url, headers=headers, json={"inputs": text})
            if hf_response.status_code == 200:
                hf_result = hf_response.json()  # Process the result if needed
                print(hf_result)  # For debugging or further processing

        # Convert text to speech using Coqui TTS
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            tts_kwargs = {
                "text": text,
                "file_path": temp_audio.name,
                "speaker": speaker,
                "speed": speed
            }
            if is_multi_lingual:
                tts_kwargs["language"] = language

            tts.tts_to_file(**tts_kwargs)

        # Send back the generated speech as a file response
        response = FileResponse(open(temp_audio.name, 'rb'), content_type='audio/wav')
        response['Content-Disposition'] = 'attachment; filename="speech.wav"'

        # Clean up the temporary file
        os.unlink(temp_audio.name)

        return response

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON in request body"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# View to handle the form and display results in template
def use_hugging_face(request):
    result = None
    error = None
    if request.method == "POST":
        text = request.POST.get('text')
        if text:
            try:
                # Example API request to Hugging Face (replace with your model's endpoint)
                url = "https://api-inference.huggingface.co/models/your_model_name"
                headers = {"Authorization": f"Bearer {settings.HF_ACCESS_TOKEN}"}
                payload = {"inputs": text}
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    result = response.json()
                else:
                    error = f"Error: {response.status_code}, {response.text}"
            except requests.exceptions.RequestException as e:
                error = str(e)
        else:
            error = "No text provided."

    return render(request, 'your_template.html', {'result': result, 'error': error})
