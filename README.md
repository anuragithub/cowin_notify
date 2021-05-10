# Cowin_notify
Notifies about the availability of vaccine based on cowin api. Docker based application build with python and airflow.
Send an email based on the vaccine availability.

Prerequisites:
* Python installation (prefereably python 3.6 and above)
* Docker installed
* Make (http://gnuwin32.sourceforge.net/packages/make.htm) [Optional]. Can run the commands from the make file one by one as well

Configuration:
* Configure the email address of sender with app-password. (File -> docker-compose.yml -> line 56-57) 
  For gmail adding app-password(hashed one) refer here ->https://security.google.com/settings/security/apppasswords
* Add the location ie district and state in `airflow_dag\cowin_dags.py` file -> line 58-62
* Add the reciever email-ids in the same file above -> line 78-79

Run:
* After installation of prerequisites above, run the cmds below from any terminal:
    1. `make build_package`
    2. `make build_docker_run` 
