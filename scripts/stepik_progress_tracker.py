import os
import re
import requests
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

def get_stepik_token():
    """Получение токена доступа к API Stepik."""
    auth = requests.auth.HTTPBasicAuth(
        os.getenv('STEPIK_CLIENT_ID'),
        os.getenv('STEPIK_CLIENT_SECRET')
    )
    response = requests.post(
        'https://stepik.org/oauth2/token/',
        data={'grant_type': 'client_credentials'},
        auth=auth
    )
    response.raise_for_status()
    return response.json().get('access_token')

def get_course_progress(course_id, token):
    """Получение прогресса курса по его ID."""
    headers = {'Authorization': f'Bearer {token}'}
    url = f'https://stepik.org/api/courses/{course_id}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    course_data = response.json()  # Преобразуем ответ в JSON

    # Проверяем, что данные о курсе получены
    if 'courses' in course_data and course_data['courses']:
        course = course_data['courses'][0]
        n_steps = course.get('total_units', 0)  # Общее количество шагов

        # Поле progress — это строка, извлекаем только первую часть (пройденные шаги)
        progress = course.get('progress', '0-0')
        n_steps_passed = int(progress.split('-')[0])  # Пройденные шаги

        return f"{n_steps_passed}/{n_steps}"
    return "0/0"

def update_progress_md(file_path, course_name, new_progress):
    """Обновление строки прогресса в файле progress.md."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    # Регулярное выражение для поиска строки с прогрессом курса
    pattern = re.compile(rf"(\| \[{re.escape(course_name)}.*?\| )(\d+/\d+)( \|)")
    updated_content = []

    for line in content:
        # Если строка содержит прогресс курса, обновляем его
        match = pattern.search(line)
        if match:
            # Используем форматирование строки вместо сырых ссылок на группы
            updated_line = f"{match.group(1)}{new_progress}{match.group(3)}\n"
            updated_content.append(updated_line)
        else:
            updated_content.append(line)

    # Перезаписываем файл с обновленным содержимым
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(updated_content)

if __name__ == "__main__":
    try:
        # Получение токена и данных о прогрессе
        token = get_stepik_token()
        course_id = os.getenv('STEPIK_COURSE_ID')
        course_name = "Data Science Starter"  # Название курса в progress.md
        progress_md_path = r"c:\Users\Dima\Way2MLE\Way2MLE\progress.md"

        # Получение актуального прогресса
        new_progress = get_course_progress(course_id, token)

        # Обновление файла progress.md
        update_progress_md(progress_md_path, course_name, new_progress)
        print("Progress updated successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")