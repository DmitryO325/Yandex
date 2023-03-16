from requests import get, post, delete

print(delete('http://localhost:8080/api/jobs/36').json())
print(get('http://localhost:8080/api/jobs/1').json())
print(get('http://localhost:8080/api/jobs/10215').json())
print(get('http://localhost:8080/api/jobs/wefef').json())
