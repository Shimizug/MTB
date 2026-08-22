#!/bin/sh
set -eu

cd "$(dirname "$0")"

if [ ! -f .env ]; then
  echo ".envがありません。先に sh 00_init.sh を実行してください。"
  exit 1
fi

echo "警告: PostgreSQLを含む、このComposeプロジェクトの全ボリュームを削除します。"
printf "DBを作り直しますか？ [y/N]: "
read -r answer

case "$answer" in
  y|Y|yes|YES)
    ;;
  *)
    echo "キャンセルしました。"
    exit 0
    ;;
esac

podman compose down --volumes --remove-orphans
podman compose up -d --build
podman compose ps

echo "DBを再作成しました。既存データは復元できません。"
