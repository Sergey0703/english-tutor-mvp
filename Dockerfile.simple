FROM python:3.11-slim

# ========== INSTALL SYSTEM DEPENDENCIES ==========
RUN apt-get update && apt-get install -y \
    # Audio/Video processing
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# ========== WORKDIR ==========
WORKDIR /app

# ========== PYTHON DEPENDENCIES ==========
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ========== COPY APPLICATION ==========
COPY agent.py .

# ========== ENVIRONMENT VARIABLES ==========
ENV PYTHONUNBUFFERED=1

# ========== EXPOSE PORTS ==========
EXPOSE 7860

# ========== START AGENT ==========
CMD ["python", "agent.py", "start"]
