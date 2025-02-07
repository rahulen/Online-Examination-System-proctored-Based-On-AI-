from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from teacher import models as TMODEL
from flask import jsonify
global username

#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')

def student_signup_view(request):
    global username
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()

            username = user.first_name

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    }
    global username
    username = request.user.first_name
    return render(request,'student/student_dashboard.html',context=dict)



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_material_view(request):
    courses=TMODEL.Material.objects.all()
    return render(request,'student/student_material.html',{'courses':courses})



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_blog_view(request):
    courses=TMODEL.Blog.objects.all()
    return render(request,'student/student_blog.html',{'courses':courses})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_exam.html',{'courses':courses})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'student/take_exam.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks})


global imageSaverCount
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request,pk):
    global imageSaverCount
    course=QMODEL.Course.objects.get(id=pk)
    questions=QMODEL.Question.objects.all().filter(course=course)
    if request.method=='POST':
        pass
    response= render(request,'student/start_exam.html',{'course':course,'questions':questions})
    response.set_cookie('course_id',course.id)
    imageSaverCount = 0
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        
        total_marks=0
        questions=QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks

        # Get additional information
        violence_counter = request.POST.get('violence_counter', 0)
        detected_violence_list = request.POST.get('detected_violence_list', '')

        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.violence_counter = violence_counter
        result.detected_violence_list = detected_violence_list
        result.save()
        print(result)

        return HttpResponseRedirect('view-result')



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/view_result.html',{'courses':courses})
    

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'student/check_marks.html',{'results':results})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_marks.html',{'courses':courses})


import random
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
 
@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def chat_msg(request,message):
    user_message = message
    print(user_message)
    if user_message=="undefined":
        return JsonResponse({'status': 'OK', 'answer': "Hello! Welcome to <b>Club.</b> I am <b>AI</b> bot tell me How can I assist you today? "}, status=status.HTTP_200_OK)

    else:
        faqBotResponse = get_response(user_message)
        if faqBotResponse[0][0][0] >=0.6:
            print('faqBotResponse',faqBotResponse)
            return JsonResponse({'status': 'OK', 'answer': faqBotResponse[1]}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'status': 'OK', 'answer': "Sorry I was not able to get your query please try again !!!"}, status=status.HTTP_200_OK)


# Import mimetypes module
import mimetypes
# import os module
import os
# Import HttpResponse module
from django.http.response import HttpResponse
# Import render module
from django.shortcuts import render


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
# Define function to download pdf file using template
def download_pdf_file(request, filename=''):
    if filename != '':
        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        filepath = BASE_DIR + "/static/study_material/"+ filename
        print(filepath)
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        return response
    





# ml_api/views.py
from django.http import JsonResponse
import student.face_emotion_detector as face_emotion_detector

 
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import io
import numpy as np
from PIL import Image
import cv2
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import numpy as np 
import base64
import cv2
import numpy as np
import torch
from pathlib import Path
from PIL import Image
import numpy as np
import cv2

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5:master', 'yolov5s')  # You can change 'yolov5s' to other variants like 'yolov5m', 'yolov5l', 'yolov5x'

def yolov5Detection(img):
    # Convert OpenCV BGR image to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Convert to PIL Image
    pil_img = Image.fromarray(img_rgb)

    # Make prediction using YOLOv5
    results = model(pil_img)

    # Extract results
    pred = results.pred[0]

    height, width, _ = img.shape
    is_violence = False
    violence_type = "Nonviolence"
    person_count = 0

    font = cv2.FONT_HERSHEY_PLAIN

    for det in pred:
        label = model.names[int(det[5])]
        print(label)

        if label == "person":
            person_count += 1

        if label in ["backpack", "umbrella", "handbag", "cell phone", "book"]:
            is_violence = True
            violence_type = "Prohibited objects"

        conf = det[4]
        box = det[0:4]
        x, y, w, h = map(int, box)

        color = (0, 255, 0)
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)  # Fix here
        cv2.putText(img, label, (x, y + 50), font, 2, color, 2)

    if person_count >= 2:
        violence_type = 'Multiple Person Detected'
        is_violence = True

    if person_count == 0:
        violence_type = "No Person Detected"
        is_violence = True

    return img, is_violence, violence_type

# Example usage:
# processed_frame, is_violence, violence_type = yolov5Detection(cap_image)
from datetime import datetime

def process_emotion(request):
    global username,imageSaverCount

    if request.method == 'POST':

        frame_file = request.FILES.get('frame', None)
        if frame_file is not None:
            frame = frame_file.read()

            # Specify the base folder path where you want to organize images
            base_folder = "violence"

            # Create a folder for the username if it doesn't exist
            user_folder = os.path.join(base_folder, username+"/face")
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)
                print(f"Created folder for user {username}")

            # Get the current timestamp
            timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
            # Convert the byte string to a numpy array
            nparr = np.frombuffer(frame, np.uint8)
            cap_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if imageSaverCount ==10:
                imageSaverCount = 0
                try:
                    timestamp1 = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                    # Specify the 
                    # file name with extension
                    file_name =  base_folder+"/"+ username+"/face/"+f"{username}_face_{timestamp1}.jpg"
                    print(file_name)
                    cv2.imwrite(file_name, cap_image)
                except Exception as e:print(e)
            else:imageSaverCount = imageSaverCount +1     

            # Process the frame and make emotion predictions
            # processed_frame, emotion_prediction = face_emotion_detector.identify_emotion(cap_image)
            processed_frame,is_voilence,voilence_type = yolov5Detection(cap_image)
            # processed_frame = cap_image
            # is_voilence = False
            # voilence_type = ""

            # print(emotion_prediction)
            
            # Convert processed_frame to base64-encoded string
            _, img_encoded = cv2.imencode('.jpg', processed_frame)
            processed_frame_base64 = base64.b64encode(img_encoded).decode('utf-8')

            # Prepare response data
            response_data = {
                'result': str(is_voilence),
                'voilence_type': voilence_type,
                'processed_frame': processed_frame_base64,
            }

            if is_voilence:

                # Specify the base folder path where you want to organize images
                base_folder = "violence"

                # Create a folder for the username if it doesn't exist
                user_folder = os.path.join(base_folder, username)
                if not os.path.exists(user_folder):
                    os.makedirs(user_folder)
                    print(f"Created folder for user {username}")

            # Get the current timestamp
                timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")

                # Specify the file name with extension
                file_name = f"{username}_{voilence_type}_{timestamp}.jpg"

                # Join the user folder path and file name
                file_path = os.path.join(user_folder, file_name)
                img_bytes = base64.b64decode(processed_frame_base64)

                # Write the image bytes to the file
                with open(file_path, 'wb') as file:
                    file.write(img_bytes)

            

            return JsonResponse(response_data)

        else:
            return JsonResponse({'error': 'Frame not found in request'})
        
    return JsonResponse({'error': 'Invalid request method'})
