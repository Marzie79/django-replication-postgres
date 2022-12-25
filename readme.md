# This is a very simple project for using replication postgresql.
## I used master for writing operations and using one of replica randomely for reading part.

For using this project, you should set database at first:
```
docker compose up
```
After running docker correctly create project's database and user so you should connect to master:
```
psql -h 127.0.0.1 -U postgres -p 5432
```
Terminal ask you postgres password and after passing password, you should create a database and a user for the app:
```
create database djnago_cqrs_db;
create user djnago_cqrs_role with encrypted password '123456789';
alter database name owner to djnago_cqrs_role;
```
Now you have a database and you can run the app:
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```