from django.shortcuts import render,redirect
from django.http import HttpResponse
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer 
import pickle
import numpy as np
import pandas as pd
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt
import pytesseract
from PIL import Image
# Create your views here.

with open(r"pickle/toxic_vect.pkl", "rb") as f:
    tox = pickle.load(f)

with open(r"pickle/severe_toxic_vect.pkl", "rb") as f:
    sev = pickle.load(f)

with open(r"pickle/obscene_vect.pkl", "rb") as f:
    obs = pickle.load(f)

with open(r"pickle/insult_vect.pkl", "rb") as f:
    ins = pickle.load(f)

with open(r"pickle/threat_vect.pkl", "rb") as f:
    thr = pickle.load(f)

with open(r"pickle/identity_hate_vect.pkl", "rb") as f:
    ide = pickle.load(f)

# Load the pickled RDF models
with open(r"pickle/toxic_model.pkl", "rb") as f:
    tox_model = pickle.load(f)

with open(r"pickle/severe_toxic_model.pkl", "rb") as f:
    sev_model = pickle.load(f)

with open(r"pickle/obscene_model.pkl", "rb") as f:
    obs_model  = pickle.load(f)

with open(r"pickle/insult_model.pkl", "rb") as f:
    ins_model  = pickle.load(f)

with open(r"pickle/threat_model.pkl", "rb") as f:
    thr_model  = pickle.load(f)

with open(r"pickle/identity_hate_model.pkl", "rb") as f:
    ide_model  = pickle.load(f)


def index(request):
    return render(request, 'index.html')

@csrf_exempt
def user_login(request):
    success_message = None
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                success_message = f'Welcome, {user.username}!'
            else:
                messages.error(request, 'Invalid username or password.')
        except Exception as e:
            print("Error:", e)
            messages.error(request, "An error occurred while processing your request.")

    return render(request, 'login.html', {'success_message': success_message})



def chart(request):
    return render(request, 'chart.html')

def performance(request):
    return render(request, 'performance.html')


def toxic(request):
    return render(request, 'toxic.html')

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        try:
            if 'text' in request.POST:
                user_input = request.POST.get('text')
                data = [user_input]
            else:
                uploaded_file = request.FILES.get('datasetfile')
                if uploaded_file:
                    extracted_text = extract_text_from_image(uploaded_file)
                    if extracted_text:
                        data = [extracted_text]
                    else:
                        return HttpResponse("Failed to extract text from the image")
                else:
                    return HttpResponse("No input data received")

            vect = tox.transform(data)
            pred_tox = tox_model.predict_proba(vect)[:,1]

            vect = sev.transform(data)
            pred_sev = sev_model.predict_proba(vect)[:,1]

            vect = obs.transform(data)
            pred_obs = obs_model.predict_proba(vect)[:,1]

            vect = thr.transform(data)
            pred_thr = thr_model.predict_proba(vect)[:,1]

            vect = ins.transform(data)
            pred_ins = ins_model.predict_proba(vect)[:,1]

            vect = ide.transform(data)
            pred_ide = ide_model.predict_proba(vect)[:,1]

            out_tox = round(pred_tox[0], 2)
            out_sev = round(pred_sev[0], 2)
            out_obs = round(pred_obs[0], 2)
            out_ins = round(pred_ins[0], 2)
            out_thr = round(pred_thr[0], 2)
            out_ide = round(pred_ide[0], 2)

            return render(request, 'prediction_preview.html', {
                'pred_tox': 'Toxic: {}'.format(out_tox),
                'pred_sev': 'Severe Toxic: {}'.format(out_sev),
                'pred_obs': 'Obscene: {}'.format(out_obs),
                'pred_ins': 'Insult: {}'.format(out_ins),
                'pred_thr': 'Threat: {}'.format(out_thr),
                'pred_ide': 'Identity Hate: {}'.format(out_ide),
            })
        except Exception as e:
            print("Error:", e)
            return HttpResponse("An error occurred while processing the request")

def extract_text_from_image(uploaded_file):
    try:
        with Image.open(uploaded_file) as img:
            # Use pytesseract to perform OCR on the image
            text = pytesseract.image_to_string(img)
            if text:
                return text
            else:
                print("No text extracted from the image")
                return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


def register(request):
    success_message = None
    
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            # Perform validation checks
            if not (username and email and password1 and password2):
                messages.error(request, "All fields are required.")
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email address is already registered.")
            else:
                # Create user
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                success_message = f'Account created for {username}! You can now log in.'
        except Exception as e:
            # Handle any other exceptions that might occur
            print("Error:", e)
            messages.error(request, "An error occurred while processing your request.")
    
    return render(request, 'register.html', {'success_message': success_message})

def logout_view(request):
    logout(request)
    return redirect('index')
