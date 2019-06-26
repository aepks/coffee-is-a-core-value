#How to install and run this project

This is written to run on a Raspberry Pi, so some instructions may be incorrect if you're on Windows.

1. `psycopg2` has some native dependencies because it compiles when you install with `pip`.  On Linix, run `sudo apt install libpq-dev python3-dev`.
2. Set up a `virtualenv` into which this project's dependencies will be installed.  This keeps packages installed on the system at large from interfering, and vice-versa.  In the main folder of the project, run `virtualenv -p python3 env` to make an `env/` folder.
3. Start up the virtualenv with `. env/bin/activate`.
4. Install Python requirements with `pip install -r requirements.txt`.

After adding a new dependency, run `pip freeze > requirements.txt`.