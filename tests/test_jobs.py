from requests import get, post, delete

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
print(delete('http://localhost:5000/api/v2/jobs/1').json())
print(get('http://localhost:5000/api/v2/jobs').json())