#!/usr/bin/env bash

set -e

REPO_URL="https://github.com/Amplicode/spring-skills.git"
BASE_DIR="$HOME/.agents"
REPO_DIR="$BASE_DIR/.amplicode/spring-skills"
TARGET_DIR="$BASE_DIR/skills"

echo "== Amplicode Spring Skills Installer =="

mkdir -p "$BASE_DIR/.amplicode"
mkdir -p "$TARGET_DIR"

# --- Git sync ---
if [ -d "$REPO_DIR/.git" ]; then
  echo "✔ Repo exists, pulling latest..."
  git -C "$REPO_DIR" pull
else
  echo "⬇ Cloning repository..."
  git clone "$REPO_URL" "$REPO_DIR"
fi

# --- Symlinks for Codex ---
echo "🔗 Creating/updating symlinks for Codex..."

for skill_path in "$REPO_DIR/skills/"*; do
  skill_name=$(basename "$skill_path")
  target_link="$TARGET_DIR/$skill_name"

  if [ -L "$target_link" ] || [ -e "$target_link" ]; then
    echo "↻ Removing existing $skill_name"
    rm -rf "$target_link"
  fi

  ln -s "$skill_path" "$target_link"
  echo "✔ Linked $skill_name"
done

echo "✅ Codex skills ready"

# --- Claude integration ---
echo "🤖 Checking Claude CLI..."

if command -v claude >/dev/null 2>&1; then
  echo "✔ Claude found, installing plugins..."

  claude plugin marketplace add "$REPO_URL" || true
  claude plugin install spring-tools@spring-tools || true
  claude plugin update spring-tools@spring-tools || true

  echo "✅ Claude plugins ready"
else
  echo "⚠ Claude CLI not found, skipping Claude setup"
fi

echo "🎉 Done"
