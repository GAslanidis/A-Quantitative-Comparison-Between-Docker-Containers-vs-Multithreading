# Docker Containers vs Multithreading

A quantitative comparison of two ways to serve the same Flask web application concurrently:

- **Multithreading:** one Gunicorn process running the app with 20 threads
- **Containers:** 20 separate Docker containers, each running its own copy of the app

Both setups received the same workload of 20 concurrent HTTP requests. CPU and memory usage were measured with `htop`, `ps` and `docker stats`.

## Tech used

- Ubuntu 25.04 (ARM64) virtual machine on Oracle VirtualBox: 8 vCPUs, 4 GB RAM
- Docker 28.2.2
- Python, Flask 3.1.3, Gunicorn 25.1.0
- Bash, curl, htop, ps

## Results

| Metric | Multithreading (20 threads) | Docker (20 containers) |
|---|---|---|
| CPU per core, idle | 0–1% | 0–5% |
| CPU per core, under load | 5–8% | 1–5% |
| System memory, idle | 1.018 GB | 1.83 GB |
| System memory, under load | 1.02 GB | 1.83–1.84 GB |
| Memory per instance | shared by all threads | ~34.6 MiB per container |

CPU usage was similar for both models, but 20 containers used about **0.8 GB more memory** than 20 threads, because each container carries its own copy of the runtime and dependencies. Multithreading is the better fit when memory is limited. Containers are the better fit when isolation, consistent deployment and scaling matter more.

## How to run

Requires Linux with Python 3, Flask, Gunicorn, curl and Docker installed.

### Multithreading

```bash
cd src
gunicorn --threads 20 'app:create_app()'
```

In a second terminal, send 20 concurrent requests:

```bash
for i in {1..20}; do curl http://127.0.0.1:8000/hello & done; wait
```

### Docker containers

```bash
cd src
docker build -t flasktest .
for i in {1..20}; do docker run -d -p $((8000+i)):8000 flasktest; done
for i in {1..20}; do curl http://127.0.0.1:$((8000+i))/hello & done; wait
docker stats
```

Open `htop` in another terminal to watch CPU and memory while the requests run.

## Project structure

```
├── src/
│   ├── app.py                 # Flask app with a single /hello route
│   └── Dockerfile             # builds the flasktest image for the container experiment
└── docs/
    ├── docker_vs_multithreading_report.docx         # full report with setup steps and screenshots
    └── docker_vs_multithreading_presentation.pptx   # summary slides
```

## Author

George Aslanidis
