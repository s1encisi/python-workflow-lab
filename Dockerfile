# A small runtime image for the isolation exercise. Development uses .devcontainer/.
FROM python:3.11-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LAB_RUN_MODE=container
WORKDIR /app
COPY energy_lab/ ./energy_lab/
COPY data/devices.json ./data/devices.json
USER 10001:10001
CMD ["python", "-m", "energy_lab"]
