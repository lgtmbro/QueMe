# QueMe


## Getting Started
1. Clone repo and spin up a virtualenv
2. In project dir `pip install -r requirements.txt`
3. `cd app` after that `cp .env.template .env` and update the .env with your twilio specifics
4. migrate the DB (sqlite) `python manage.py migrate`
5. create admin user at `python manage.py createsuperuser`
6. `python manage.py runserver` to run server
7. login to admin panel at http://localhost:8000/admin login with admin user details you created
8. Add quesions to `Questions` table, mark them as active for the whatsapp users to answer them
9. install ngrok
10. run `ngrok http 8000`, which will create a tunnel to your local django instance from the www, please add your tunnel url to the ALLOWD_HOSTS in `.env` omit the `https://`
11. Update your twilio sandbox URLs on their website:
    * Incoming messages will be `[ngrok tunnel]/questions/twilio_messages`


That should get you going.