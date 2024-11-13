import os
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import EventForm
from .models import Event
# Директория, куда будут загружаться файлы
UPLOAD_DIR = 'uploads'
# проверяем существование директории и если она не существует, то создаем её
def ensure_upload_dir_exists():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
# функция для обработки запросов на главной странице
def index(request):
    ensure_upload_dir_exists()
# Обработка POST-запроса
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            # Сохранение данных в файл JSON
            data = {
                'name': event.name,
                'date': event.date.strftime('%Y-%m-%d'),
                'location': event.location,
                'description': event.description
            }
            file_path = os.path.join(UPLOAD_DIR, f'{event.id}.json')
            with open(file_path, 'w') as f:
                json.dump(data, f)
            return redirect('index')
    else:
        form = EventForm()
 # Получение списка файлов JSON в директории загрузки
    files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith('.json')]
    return render(request, 'index.html', {'form': form, 'files': files, 'no_files': not files})
# Функция для загрузки файлов
def upload_file(request):
    ensure_upload_dir_exists()
 # Обработка POST-запроса
    if request.method == 'POST':
        file = request.FILES['file']
        if file.name.endswith('.json'):
            file_path = os.path.join(UPLOAD_DIR, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Проверка содержимого загруженного файла
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    required_fields = ['name', 'date', 'location', 'description']
                    for field in required_fields:
                        if field not in data:
                            os.remove(file_path)  # Удаление файла, если данные неполные
                            messages.error(request, f"Отсутствует обязательное поле: {field}")
                            return redirect('upload_file')
            except json.JSONDecodeError:
                os.remove(file_path)  # Удаление файла, если он не является JSON
                messages.error(request, "Недопустимый файл JSON")
                return redirect('upload_file')

            return redirect('index')
        else:
            messages.error(request, "Недопустимый формат файла. Пожалуйста, загрузите файл в формате JSON.")
            return redirect('upload_file')
    return render(request, 'upload.html')
# Функция для просмотра содержимого файла
def view_file(request, filename):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return render(request, 'view_file.html', {'data': data})
    else:
        return HttpResponse("Файл не найден")
# Функция для просмотра всех данных из файлов JSON
def view_all_data(request):
    ensure_upload_dir_exists()
    all_data = []
    for file in os.listdir(UPLOAD_DIR):
        if file.endswith('.json'):
            file_path = os.path.join(UPLOAD_DIR, file)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    all_data.append(data)
            except json.JSONDecodeError:
                # Пропускаем некорректные файлы
                continue
    return render(request, 'view_all_data.html', {'all_data': all_data})