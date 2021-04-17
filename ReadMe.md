## Setting Up Project (Windows)

##### 1. Clone the project anywhere on the disk.ie  `D:/PythonProjects/` using the following commands

```bash
    git clone https://github.com/yasirrose/DjangoTasksApp.git TasksApp
    cd TasksApp
    python -m venv env
    .\env\Scripts\activate
    pip install -r requirements.txt
```

##### 2. Set Database credentials in `TasksApp\settings.py` file 

```python
DATABASES = {
    'default': {
        'ENGINE': os.getenv("DATABSE_ENGINE", "django.db.backends.mysql"),
        'NAME': os.getenv("DATABSE_NAME", 'tasks'),
        'USER': os.getenv("DATABSE_USER", "tasks"),
        'PASSWORD': os.getenv("DATABSE_PASSWORD", "secret"),
        'HOST': os.getenv("DATABSE_HOST", "127.0.0.1"),
        'PORT': os.getenv("DATABSE_PORT", "3306"),
    }
}
```

##### 3. Run the database migrations

```bash
python manage.py migrate
```

##### 4. Run the the project on local system

```bash
python manage.py runserver
```
This will start the development server and project will be accessible on browser on `http://localhost:8000`

For Frontend code like Css and Js we have used the `webpack` and production build is included with the app if you want to customize the `javascript` or `scss` code you will need to take this additional step

##### 5. Frontend development
Installing dependencies (Node and yarn should be installed) 

```bash
yarn
```
For development run `yarn watch` and to create the production build run the following command `yarn build` this will crate the compressed much smaller build and remove all unused CSS.

