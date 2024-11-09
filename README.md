# personal_finances
## Commands
### activate environment
source venv/bin/activate

<!-- ## conda environment
conda activate flaskProject -->

### run flask
flask --debug run

## New libraries
pip freeze > requirements.txt

Data base local

`psql -h localhost -p 5432`

## flush sockets
when: Access to 127.0.0.1 was denied

go to and flush sockets:
chrome://net-internals/#sockets

## Theoretical basis
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates

## Migrations
Generate Migration Script: Create a migration script that will generate the SQL to create the Article table:

flask db migrate -m "Create article table"

Apply the Migration: Apply the migration to your database to create the table:

flask db upgrade

## flask shell
flask shell
