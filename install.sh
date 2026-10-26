#!/usr/bin/env bash
# install.sh — install skills from this repo into supported AI agents
# Usage: ./install.sh [--dry-run] [--agent claude|all]

set -euo pipefail

SKILLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DRY_RUN=false
AGENT="all"

# ── parse args ────────────────────────────────────────────────────────────────
for arg in "$@"; do
  case $arg in
    --dry-run) DRY_RUN=true ;;
    --agent=*) AGENT="${arg#*=}" ;;
    *) echo "Unknown arg: $arg" && exit 1 ;;
  esac
done

# ── helpers ───────────────────────────────────────────────────────────────────
log()  { echo "  $*"; }
ok()   { echo "  ✓ $*"; }
skip() { echo "  ○ $*"; }
info() { echo; echo "▶ $*"; }

append_block() {
  # idempotent: skip if marker already present
  local file="$1" marker="$2" content="$3"
  if [[ -f "$file" ]] && grep -qF "$marker" "$file" 2>/dev/null; then
    skip "already in $file — skip"
    return
  fi
  if $DRY_RUN; then
    skip "[dry-run] would append to: $file"
    return
  fi
  mkdir -p "$(dirname "$file")"
  printf '\n%s\n' "$content" >> "$file"
  ok "appended: $file"
}

skill_name() {
  grep '^name:' "$1" | head -1 | sed 's/name: *//'
}

skill_body() {
  # strip YAML front matter (between first two --- lines)
  awk '/^---/{f++; next} f>=2{print}' "$1"
}

skill_description() {
  awk '
    /^description:/{found=1; next}
    found && /^  /{printf "%s ", $0; next}
    found{exit}
  ' "$1" | sed 's/^  //g; s/  */ /g; s/ *$//'
}

# ── CLAUDE ────────────────────────────────────────────────────────────────────
install_claude() {
  info "Claude Code (~/.claude/CLAUDE.md)"
  local claude_file="$HOME/.claude/CLAUDE.md"

  while IFS= read -r -d '' skill_file; do
    local name desc body marker block
    name=$(skill_name "$skill_file")
    desc=$(skill_description "$skill_file")
    body=$(skill_body "$skill_file")
    marker="<!-- skill:${name} -->"

    block="${marker}
## Skill: ${name}

> ${desc}

${body}
<!-- /skill:${name} -->"

    log "skill: $name"
    append_block "$claude_file" "$marker" "$block"
  done < <(find "$SKILLS_DIR" -name "SKILL.md" -print0 | sort -z)

  ok "Claude install done → $claude_file"
}

# ── dispatch ──────────────────────────────────────────────────────────────────
SKILL_COUNT=$(find "$SKILLS_DIR" -name "SKILL.md" | wc -l | tr -d ' ')

echo ""
echo "╔══════════════════════════════════════╗"
echo "║        skills/install.sh             ║"
echo "╚══════════════════════════════════════╝"
echo ""
log "skills root : $SKILLS_DIR"
log "agent       : $AGENT"
log "dry-run     : $DRY_RUN"
log "skills found: $SKILL_COUNT"

case "$AGENT" in
  claude|all) install_claude ;;
  *) echo "Unknown agent: $AGENT. Supported: claude, all" && exit 1 ;;
esac

echo ""
echo "Done."
