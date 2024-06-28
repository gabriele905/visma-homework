# homework assignment by Gabrielė Dumbliauskė

## Running services with docker-compose

Make sure you have docker and docker-compose on your system.

The project can be started by running the `docker-compose up --build -d` command.
All environment variables are in `.env` file.

Django app will be hosted on `127.0.0.1:1337`.

### To run unit tests:
Activate virtual environment:
```
source venv/bin/activate
```
Run tests:
```
python3 manage.py test --settings=config.test_settings
```