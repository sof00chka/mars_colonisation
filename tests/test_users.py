from requests import get, post, delete, put

print(get('http://localhost:5000/api/v2/users/999').json())
print(get('http://localhost:5000/api/v2/users/1').json())

print(delete('http://localhost:5000/api/v2/users/999').json())
print(delete('http://localhost:5000/api/v2/users/1').json())
print(get('http://localhost:5000/api/v2/users').json())

print(post('http://localhost:5000/api/v2/users', json={}).json())
print(post('http://localhost:5000/api/v2/users', json={'surname': 'Ошибкин'}).json())
print(post('http://localhost:5000/api/v2/users', json={
    'surname': 'Ошибкин', 'name': 'Тип', 'age': 'много лет',
    'position': 'dev', 'speciality': 'python',
    'address': 'MSK', 'email': 'err@test.com',
    'modified_date': '2026-05-04'
}).json())
print(post('http://localhost:5000/api/v2/users', json={
    'surname': 'Сидорова',
    'name': 'Анна',
    'age': 25,
    'position': 'Дизайнер',
    'speciality': 'UI/UX',
    'address': 'Питер',
    'email': 'anna@example.com'
}).json())

print(put('http://localhost:5000/api/v2/users/2', json={
    'surname': 'Петрова',
    'position': 'Senior Developer'
}).json())

print(put('http://localhost:5000/api/v2/users/2', json={
    'surname': 'Иванова',
    'name': 'Елена',
    'age': 28,
    'position': 'Team Lead',
    'speciality': 'Management',
    'address': 'Казань',
    'email': 'elena@example.com'
}).json())

print(get('http://localhost:5000/api/v2/users').json())