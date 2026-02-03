#!/bin/bash
set -e

echo "=== Environment Variables Debug ==="
echo "POSTGRES_HOST: ${POSTGRES_HOST:-NOT_SET}"
echo "POSTGRES_PORT: ${POSTGRES_PORT:-NOT_SET}"
echo "POSTGRES_NAME: ${POSTGRES_NAME:-NOT_SET}"
echo "POSTGRES_USER: ${POSTGRES_USER:-NOT_SET}"
echo "POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:+***SET***}"

# Eğer değişkenler boşsa hata ver
if [ -z "$POSTGRES_HOST" ] || [ -z "$POSTGRES_NAME" ] || [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_PASSWORD" ]; then
    echo "ERROR: Required environment variables are not set!"
    echo "Please set POSTGRES_HOST, POSTGRES_PORT, POSTGRES_NAME, POSTGRES_USER, and POSTGRES_PASSWORD in Coolify"
    exit 1
fi

echo "=== Creating secrets file ==="
mkdir -p .streamlit

cat > .streamlit/secrets.toml << EOF
[postgres]
host = "${POSTGRES_HOST}"
port = "${POSTGRES_PORT:-5432}"
database = "${POSTGRES_NAME}"
user = "${POSTGRES_USER}"
password = "${POSTGRES_PASSWORD}"

[app]
max_file_size = 1073741824
upload_folder = "/usr/src/app/uploads"
EOF

echo "✓ Secrets file created successfully"
echo "File content (password hidden):"
grep -v "password" .streamlit/secrets.toml || true

echo "=== Starting Streamlit ==="
exec streamlit run app.py --server.port=8502 --server.address=0.0.0.0