#!/bin/sh
set -eu

cd "$(dirname "$0")"

if [ ! -f .env ]; then
  cp .env.example .env
  echo ".env を作成しました。"
  echo "POSTGRES_PASSWORDを安全な値へ変更してから、もう一度実行してください。"
  exit 1
fi

if grep -q '^POSTGRES_PASSWORD=change-me$' .env; then
  echo ".env のPOSTGRES_PASSWORDが初期値のままです。"
  echo "安全なパスワードへ変更してから、もう一度実行してください。"
  exit 1
fi

podman compose build
podman compose up -d
podman compose ps

echo "初回起動が完了しました。"
