# Movie recommendation engine

## Setup

-----------------------------------------------------------------
#### Create virtual environment for python
Execute the below command to create virtual environment
- ``` python -m venv venv ```

Then active environment:

for windows:
- ```source venv/Scripts/activate```

for unix:
- ```source venv/bin/activate```
-----------------------------------------------------------------
#### Install requirements
Use makefile
- ```make install_requirements```

or classic
- ```pip install -r ./requirements.txt```
-----------------------------------------------------------------
#### Run app
Use makefile
- ```make run_app```

or classic
- ```python main.py```

-----------------------------------------------------------------
#### Select the name of one of the users from movie_data and pass it to the MovieEngine class. That's all.
