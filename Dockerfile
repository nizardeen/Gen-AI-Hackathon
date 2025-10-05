FROM postgres:16.4

# Copy the startup script and SQL files
COPY start.sh /docker-entrypoint-initdb.d/start.sh
COPY sql /sql
COPY data /data

RUN chmod +x /docker-entrypoint-initdb.d/start.sh