#python3 -m  pytest --capture=no tests/ b
python3 -m  pytest --cov=. --capture=no $1
#python3 -m  pytest $1