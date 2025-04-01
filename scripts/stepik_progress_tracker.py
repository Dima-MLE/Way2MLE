import requests
from datetime import datetime

# Конфигурация
COURSE_ID = 194633  # ID курса Data Science Starter
STEPIK_CLIENT_ID = 'your_client_id'  # Зарегистрируйте приложение на stepik.org/oauth2/applications
STEPIK_CLIENT_SECRET = 'your_client_secret'
PROGRESS_FILE = 'progress.md'  # Файл для обновления прогресса

def get_stepik_token():
    """Получение OAuth токена для Stepik API"""
    auth = requests.auth.HTTPBasicAuth(STEPIK_CLIENT_ID, STEPIK_CLIENT_SECRET)
    response = requests.post(
        'https://stepik.org/oauth2/token/',
        data={'grant_type': 'client_credentials'},
        auth=auth
    )
    return response.json().get('access_token')

def fetch_course_progress(course_id, token):
    """Получение данных о прогрессе курса"""
    headers = {'Authorization': f'Bearer {token}'}
    
    # Получаем информацию о курсе
    course_url = f'https://stepik.org/api/courses/{course_id}'
    course_data = requests.get(course_url, headers=headers).json()
    
    # Получаем список уроков
    lessons_url = f'https://stepik.org/api/lessons?course={course_id}'
    lessons_data = requests.get(lessons_url, headers=headers).json()
    
    # Получаем прогресс по курсу (нужна аутентификация пользователя)
    # В демо-версии используем общую информацию
    
    return {
        'title': course_data['courses'][0]['title'],
        'total_steps': course_data['courses'][0]['total_steps'],
        'lessons': len(lessons_data['lessons']),
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
    }

def update_progress_file(course_data):
    """Обновление файла прогресса"""
    with open(PROGRESS_FILE, 'r+', encoding='utf-8') as file:
        content = file.readlines()
        
        # Ищем строку с курсом для обновления
        for i, line in enumerate(content):
            if "Data Science Starter" in line:
                # Форматируем новую строку с актуальным прогрессом
                new_line = f"| [Data Science Starter](https://stepik.org/course/{COURSE_ID}/syllabus) | Stepik | [HSE](https://www.hse.ru/ma/mlds/) | {course_data['total_steps']} | 🔵 High |\n"
                content[i] = new_line
                break
        
        # Добавляем информацию о последнем обновлении
        content.append(f"\n<!-- Last updated: {course_data['last_updated']} -->\n")
        
        # Перезаписываем файл
        file.seek(0)
        file.writelines(content)
        file.truncate()

def main():
    try:
        print("Получение токена Stepik API...")
        token = get_stepik_token()
        
        print("Загрузка данных о курсе...")
        course_data = fetch_course_progress(COURSE_ID, token)
        
        print("Обновление файла прогресса...")
        update_progress_file(course_data)
        
        print(f"Готово! Курс '{course_data['title']}' обновлен.")
        print(f"Всего шагов: {course_data['total_steps']}")
        print(f"Последнее обновление: {course_data['last_updated']}")
    except Exception as e:
        print(f"Ошибка: {str(e)}")

if __name__ == "__main__":
    main()
