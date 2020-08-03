#!/usr/bin/env bash
resp="HTTP/1.1 200 OK \r\nConnection: Keep-aliver\r\n\r\n${2:-"OK"}\r\n"
while { echo -en "$resp"; } | nc -l "${1:-8080}"; do
	echo "===================="
done

