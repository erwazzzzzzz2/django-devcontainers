# Django development environment using VSCode Remote Containers

## Pre-requisites:

1. Docker 
2. VSCode
3. VSCode Dev Containers extension
4. VSCode Docker extension

## Getting the default Django project running:

Create an empty app.py file in the directory. 

Open the command palette (cmd+P on Mac, Ctrl+Shift+P on Windows), and select Docker: Add Docker Files to Workspace. It should give you a number of options, including Python: Django which is the one we want. Select Python: Django. It should then ask you for the entry point, so select the app.py file we created earlier.

It will then ask you which port you want to listen to, the default is fine.

The last one should be “Include optional Docker Compose files?”, Select 'Yes'.

Delete app.py

## Add the development container definition and connecting to it:

Open your command palette, and select Dev-Containers: Add Development Container Configuration Files. You should get a prompt asking you how you would like to create your container configuration, and you should choose from docker-compose.yml. This should create a .devcontainer folder, with devcontainer.json inside it.

Open your command palette again, and select Dev-Containers: Rebuild and Reopen in Container

You should see another window open with a number of things running. This is just VSCode setting up your development container. Wait until it’s done.

## Generate your Django project:

Open a terminal if it isn't alreay open an use the commands 
``` $ django-admin startproject testproject . ```
``` $ python manage.py runserver ```

Check default page on http://127.0.0.1:8000

### Add Postgres

In your docker-compose.yml file you should add one service for Postgres. 
```

version: '3.4'

services:
  testproject:
    image: testproject
    build:
      context: .
      dockerfile: ./Dockerfile
    ports:
      - 8000:8000
    depends_on:
      - postgresdb
  postgresdb:
    image: postgres
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - 5432:5432
    environment:
      - POSTGRES_DB=testproject
      - POSTGRES_USER=testproject
      - POSTGRES_PASSWORD=hello

volumes:
  pgdata:

```

Modify settings.py to point to the Postgres container (in production these values should ideally be read from environment variables):

```

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'testproject',
        'USER': 'testproject',
        'PASSWORD': "hello",
        'HOST': "postgresdb",
        'PORT': '5432',
        'CONN_MAX_AGE': 60,
    }
}

```

Add psycopg2-binary to your requirements.txt file, and pin it to the most recent version

Rebuild and reopen the container again

## Check your set up 

1. In the terminal use pip freeze to see dependencies
2. In terminal run cat /etc/os-release  which should show the OS as Debian (the image OS) . This shows you are in the container. Or use printenv $DOCKER_RUNNING.

## Add formatting and Linting

Add the following to the evcontainers.json (see known issue (2))

	 "customizations": {
		"vscode": {
			"settings": {
				"[python]": {
					"editor.tabSize": 4,
					"editor.formatOnSave": true,
					"editor.codeActionsOnSave": {
							"source.organizeImports": true
					}
				}
			},
			"extensions": [
				"ms-python.python",
				"ms-python.black-formatter",
				"ms-python.isort",
				"ms-python.flake8",
				"ms-azuretools.vscode-docker"
			]

   
## Know Issues:

1. Sometimes I’ve found that VSCode would fail to forward the port automatically now that we’ve published port 8000 in the docker-compose.yml, which conflicts with the port forwarding feature. In that case you should try runserver by binding to 0.0.0.0, i.e. python manage.py runserver 0.0.0.0:8000. Or alternatively, you could also just remove ports from the docker-compose.yml file.

2. When formatting and linting are enable you will be requeste to install the Python extension of VSCode. This appears to be a bug where the extension is slow / isn't installed as it should be and the manual install is required see [GitHun Issue 1967784](https://github.com/microsoft/vscode/issues/196794)
   
   




