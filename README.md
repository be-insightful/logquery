# 로그 조회 API
[FastAPI](https://fastapi.tiangolo.com/) 프레임워크를 사용하여 RestAPI를 개발.  
post request를 받으면 elasticsearch에서 요청 받은 데이터를 찾아 json 형태로 response 함.

## working directory
`logquery`


## containers
- logquery
- traefix: reverseproxy 역할을 함. https적용, domain주소 적용에 사용.

## run
```bash
docker-compose up -d
```