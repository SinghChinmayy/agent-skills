#!/usr/bin/env bash

# OG image generator skill
# Generates two OG image variants (A and B) using headless Chrome.
# Outputs PNGs to scripts/tmp/og/ and 300px previews.

# Resolve project root (assumes this script lives in skills/og-generator)
PROJECT_ROOT=$(cd "$(dirname "$0")/../.. && pwd)
OUTPUT_DIR="$PROJECT_ROOT/scripts/tmp/og"
mkdir -p "$OUTPUT_DIR"

# Templates
TEMPLATE_A="$PROJECT_ROOT/skills/og-generator/template-a.html"
TEMPLATE_B="$PROJECT_ROOT/skills/og-generator/template-b.html"

# Chrome flags (macOS)
CHROME="$(ls -1 /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome 2>/dev/null || echo "")"
if [[ -z "$CHROME" ]]; then
  echo "Chrome not found. Please install Google Chrome." >&2
  exit 1
fi

run_chrome() {
  local template=$1
  local out_png=$2
  "$CHROME" \
    --headless \
    --disable-gpu \
    --no-sandbox \
    --allow-file-access-from-files \
    --disable-web-security \
    --window-size=1200,630 \
    --screenshot="$out_png" \
    "file://$template"
}

# Generate full-size PNGs
run_chrome "$TEMPLATE_A" "$OUTPUT_DIR/variant-a.png"
run_chrome "$TEMPLATE_B" "$OUTPUT_DIR/variant-b.png"

# Generate 300px wide previews (preserve aspect ratio)
sips -Z 300 "$OUTPUT_DIR/variant-a.png" --out "$OUTPUT_DIR/variant-a-preview.png"
sips -Z 300 "$OUTPUT_DIR/variant-b.png" --out "$OUTPUT_DIR/variant-b-preview.png"

# Verify dimensions
echo "--- Variant A info ---"
sips -g pixelWidth -g pixelHeight "$OUTPUT_DIR/variant-a.png"
ls -l "$OUTPUT_DIR/variant-a.png"

echo "--- Variant B info ---"
sips -g pixelWidth -g pixelHeight "$OUTPUT_DIR/variant-b.png"
ls -l "$OUTPUT_DIR/variant-b.png"

exit 0
