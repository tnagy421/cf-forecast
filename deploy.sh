#!/bin/bash

# 🚀 Deployment Script - 13-Week Cash Flow Forecast
# Tento skript pushne aplikáciu na GitHub a deployuje na Streamlit Cloud
# Pre macOS/Linux

echo "╔════════════════════════════════════════════════════╗"
echo "║  13-Week Cash Flow Forecast - Deployment Script   ║"
echo "╚════════════════════════════════════════════════════╝"

# 1. Overenie Git a GitHub CLI
echo ""
echo "📋 Overovanie... "
if ! command -v git &> /dev/null; then
    echo "❌ Git nie je nainštalovaný. Nainštalujte git: https://git-scm.com/download"
    exit 1
fi
echo "✅ Git nájdený"

# 2. Navigácia do zložky
echo ""
echo "📁 Navigácia do cf-forecast..."
cd cf-forecast || {
    echo "❌ Zložka 'cf-forecast' nenájdená!"
    echo "Vytvorte ju a skopírujte súbory."
    exit 1
}

# 3. Git status
echo ""
echo "📊 Git status:"
git status

# 4. Git push
echo ""
echo "🚀 Pushuje sa do GitHub..."
echo "Zadajte GitHub username: $"
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Úspešne pushnuté na GitHub!"
    echo ""
    echo "╔════════════════════════════════════════════════════╗"
    echo "║  🎉 Ďalší krok: Deploy na Streamlit Cloud        ║"
    echo "╚════════════════════════════════════════════════════╝"
    echo ""
    echo "1. Choďte na https://streamlit.io/cloud"
    echo "2. Prihláste sa s GitHub účtom (tnagy421)"
    echo "3. Kliknite 'New app'"
    echo "4. Vyberte repo: tnagy421/cf-forecast"
    echo "5. Vyberte branch: main"
    echo "6. Nastavte main file path: app.py"
    echo "7. Kliknite 'Deploy'"
    echo ""
    echo "Vaša aplikácia bude dostupná na:"
    echo "https://cf-forecast-XXXXX.streamlit.app"
else
    echo "❌ Push zlyhal. Skontrolujte:"
    echo "  - GitHub token je platný"
    echo "  - Internet pripojenie"
    echo "  - Git je nakonfigurovaný"
fi
