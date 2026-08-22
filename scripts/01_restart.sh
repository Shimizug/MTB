#!/bin/sh
set -eu

cd "$(dirname "$0")"

if [ ! -f .env ]; then
  echo ".envがありません。先に sh 00_init.sh を実行してください。"
  exit 1
fi

podman compose down
podman compose up -d --build
podman compose ps

echo "アプリケーションを再起動しました。"
