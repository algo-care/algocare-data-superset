### Algocare-Superset

- 변경 내용
  - /docker
    - .env-non-dev 
      - Google OAuth 사용하기 위한 GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET 값 추가
    - requirements-local.txt
      - Google OAuth 사용하기 위한 Authlib 추가 설치
  - /docker/python_dev 
    - superset_config.py
      - GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET 값 추가
      - Max row 세팅
      - Default 권한 admin 으로 세팅
    - custom_sso_security_manager.py
      - SSO Manger 추가
      - Google Oauth 사용시 코드오류로 필요시 디버깅
