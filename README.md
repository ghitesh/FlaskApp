# FlaskApp
This a Flask based microservices Example App

How to run this..hopefully ;)

activate venv

pip install requirements


====
PyCharm -> VCS -> Get from version control.
In preferences add interpreter to add venv

Make and change in requirements.txt, same and open any py file. You'll be asked to install requirements. Install All.

Open 4 terminal windows and cd to the ProjectDir

Run following commands:
===== Terminal 1 ======
. venv/bin/activate
export FLASK_ENV=development
export FLASK_PORT=8001
export FLASK_APP=application/main_user
flask run -p $FLASK_PORT

===== Terminal 2 ======
. venv/bin/activate
export FLASK_ENV=development
export FLASK_PORT=8002
export FLASK_APP=application/main_hospital
flask run -p $FLASK_PORT

===== Terminal 3 ======
. venv/bin/activate
export FLASK_ENV=development
export FLASK_PORT=8003
export FLASK_APP=application/main_test_center
flask run -p $FLASK_PORT


===== Terminal 4 (For running test cases ======
. venv/bin/activate
python3 -m pytest application/tests_routes.py -W ignore --junitxml=unit.xml -o junit_family=xunit1


