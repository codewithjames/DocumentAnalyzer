#####Overview of features:

- Docker & Docker-Compose - Environment variables, logging, etc.
- Django
- Nginx proxy for static and dynamic content
- SQLite for data storage/retrieval
- asyncio concurrency programming for file proecessing

#### Core Images/Components:
3. Django
4. Nginx

## Build Process

- Docker is a requirement to run the project at this time, as is an external network connection to pull down images and fetch domains.

1. docker-compose up --build --no-start
2. docker-compose start

#### Notes
- Logs are stored in the logs folder in the current directory!
- When build is run the Django tests are executed
- Server is accessed at port 8000, Django is proxied from port 8080 (also accessible but without static files)
- If you go to say http://127.0.0.1:8000 the url in DRF API Root won't include the port (8000)


###Interaction

To upload a file, post it to http://127.0.0.1:8000/upload/ and the response will include the metrics. For all metrics you can go to http://127.0.0.1:8000/metrics/ for a list or to a specific metric at http://127.0.0.1:8000/metrics/1/