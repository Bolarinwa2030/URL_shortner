# URL Shortener

![CI Pipeline](https://github.com/Bolarinwa2030/URL_shortner/actions/workflows/ci.yml/badge.svg)

A production-grade URL shortener built with FastAPI, PostgreSQL, Redis, 
Docker, and GitHub Actions CI/CD.

## Stack
- FastAPI — REST API
- PostgreSQL — persistent storage
- Redis — cache layer (cache-aside pattern)
- Docker + Docker Compose — containerisation
- GitHub Actions — CI/CD pipeline
- Docker Hub — container registry

## Quick Start
git clone https://github.com/Bolarinwa2030/URL_shortner.git
cd URL_shortner
docker compose up --build

API runs at http://localhost:8000
Docs at http://localhost:8000/docs