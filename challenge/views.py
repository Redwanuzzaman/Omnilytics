import os
import random
import string
from django.shortcuts import render
from django.http import HttpResponse
import json
import mimetypes


def generate_random_objects():
    alphabatic = ''.join(
        random.choice(string.ascii_lowercase) for i in range(8))  # Generating random string upto 8 character
    alphanumeric = ''.join(random.choices(string.ascii_letters, k=4) + random.choices(string.digits, k=4))  # Generating random aplhanumeric string upto 8 character
    integer = random.randint(0, 100000000)  # For generating random integer between 0 to 100000000
    real_number = random.uniform(1.0, 10.0)
    return alphabatic, integer, real_number, alphanumeric


def write_to_file():
    try:
        with open('challenge/challenge.txt', 'w+') as file:
            size = os.path.getsize('challenge/challenge.txt') / 1024 / 1024  # Converting Byte to MB
            while float(size) <= 2.0:
                alpha, integer, real, alphanum = generate_random_objects()
                data = f'{alpha},{integer},{real},{alphanum} \n'
                file.write(data)
                size = os.path.getsize('challenge/challenge.txt') / 1024 / 1024
        return True
    except Exception as e:
        return False


def index(request):
    if request.POST:
        res = write_to_file()
        return HttpResponse(json.dumps({'status': 200 if res else 500}))
    return render(request, "challenge/index.html")


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def read_from_file():
    with open('challenge/challenge.txt', 'r') as file:
        alpha_count = alphanum_count = digit_count = real_num_count = 0
        for line in file:
            data = line.split(',')
            for i in data:
                if i.isdigit():
                    digit_count += 1
                elif isfloat(i):
                    real_num_count += 1
                elif i.isalpha():
                    alpha_count += 1
                else:
                    alphanum_count += 1
    return {'alpha': alpha_count, 'alphanum': alphanum_count, 'digit': digit_count, 'real': real_num_count}


def download_file(request, **kwargs):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'challenge.txt'
    # Define the full file path
    filepath = BASE_DIR + '/challenge/' + filename
    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response


def report(request, **kwargs):
    data = read_from_file()
    return HttpResponse(json.dumps(data))
