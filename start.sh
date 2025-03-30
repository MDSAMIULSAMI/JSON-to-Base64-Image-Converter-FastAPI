#!/bin/bash
uvicorn fastapi_json_to_image:app --host 0.0.0.0 --port $PORT
