from requests import get, post, delete, put

print(get('http://localhost:5000/api/v2/jobs/999').json())
print(get('http://localhost:5000/api/v2/jobs/1').json())

print(post('http://localhost:5000/api/v2/jobs', json={}).json())
print(post('http://localhost:5000/api/v2/jobs', json={'team_leader': 1}).json())
print(post('http://localhost:5000/api/v2/jobs', json={
    'team_leader': 1, 'job': 'Ошибка', 'work_size': 'много',
    'collaborators': '1, 2, 3', 'start_date': '2026-05-04 10:00:00',
    'end_date': '2026-05-05 18:00:00', 'is_finished': False
}).json())
print(post('http://localhost:5000/api/v2/jobs', json={
    'team_leader': 2, 'job': 'Разработка модуля', 'work_size': 25,
    'collaborators': '4, 5', 'start_date': '2026-05-06 09:00:00',
    'end_date': '2026-05-10 17:00:00', 'is_finished': True
}).json())
print(get('http://localhost:5000/api/v2/jobs').json())

print(put('http://localhost:5000/api/v2/jobs/2', json={
    'job': 'Обновленная задача',
    'work_size': 30
}).json())

print(put('http://localhost:5000/api/v2/jobs/2', json={
    'team_leader': 3,
    'job': 'Полностью обновленная задача',
    'work_size': 40,
    'collaborators': '6, 7, 8',
    'start_date': '2026-05-07 10:00:00',
    'end_date': '2026-05-12 18:00:00',
    'is_finished': False
}).json())

print(delete('http://localhost:5000/api/v2/jobs/1').json())
print(get('http://localhost:5000/api/v2/jobs').json())