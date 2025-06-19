# This is a clone off this project: https://github.com/jakerieger/FlaskIntroduction.git, dockerized.

## Before:
- How To Run
1. Install `virtualenv`:
```
$ pip install virtualenv
```
2. Open a terminal in the project root directory and run:
```
$ virtualenv env
```
3. Then run the command:
```
$ .\env\Scripts\activate
```
4. Then install the dependencies:
```
$ (env) pip install -r requirements.txt
```
5. Finally start the web server:
```
$ (env) python app.py
```
This server will start on port 5000 by default. You can change this in `app.py` by changing the following line to this:
```python
if __name__ == "__main__":
    app.run(debug=True, port=<desired port>)
```

## After:
1. Install Docker
```
https://docs.docker.com/engine/install/
```
3. Run:
```
$ docker compose up --build #To see the logs
```
or:
```
$ docker compose up -d --build #To avoid seeing the logs
```
This server will start on port 5000 by default. You can change this in `app.py` by changing the following line to this:
```python
if __name__ == "__main__":
    app.run(debug=True, port=<desired port>)
```
Once the containers are running, you can access the API at http://localhost:5000 and the Prometheus dashboard at http://localhost:9090. The /metrics endpoint of the API will expose the metrics that Prometheus can scrape.

## Contributing

Since this is a repository for a tutorial, the code should remain the same as the code that was shown in the tutorial. Any pull requests that don't address security flaws or fixes for language updates will be automatically closed. Style changes, adding libraries, etc are not valid changes for submitting a pull request.

## References:
- https://github.com/jakerieger/FlaskIntroduction.git
- https://medium.com/@letathenasleep/exposing-python-metrics-with-prometheus-c5c837c21e4d
- https://medium.com/@abderraoufbenchoubane/setup-a-python-environment-with-docker-a4e38811e0d3
- https://stackoverflow.com/questions/17042201/how-to-style-input-and-submit-button-with-css
  
..thanks!
