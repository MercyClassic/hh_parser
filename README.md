<h1> ABOUT </h1>
<h3> <a> headhunter.ru </a> parser that notifying about new probable vacancy </h3>

<h1> SETUP </h1>


<h2> CREATE VENV </h2>

```
poetry install
```

<h3> or </h3>

```
pip install -r requirements.txt
```

<h2> CREATE DB </h2>

```
alembic upgrade head
```

<h2> CREATE ENV FILE </h2>

```
BOT_TOKEN=...  # telegram bot token
TO_NOTIFICATE=...  # telegram id

```

<h2> RUN SCRIPT </h2>

```
cd src && python main.py
```
