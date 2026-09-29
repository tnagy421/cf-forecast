# 🚀 Deployment Guide - Streamlit Cloud

**Status**: ✅ Kód je pripravený na GitHub  
**Čas**: ~10 minút  
**Náročnosť**: ⭐⭐ Ľahké

---

## 📋 Čo máte už hotovo:

✅ Všetky aplikačné súbory sú v `cf-forecast` repo  
✅ `.gitignore` nakonfigurovaný  
✅ `.streamlit/config.toml` pripravený  
✅ Git repo inicializovaný a committed

---

## 🎯 2 Spôsoby ako deployovať:

### **SPÔSOB 1: Automaticky (Odporúčané)**

#### Na macOS/Linux:
```bash
cd cf-forecast
chmod +x deploy.sh
./deploy.sh
```

#### Na Windows:
```bash
cd cf-forecast
deploy.bat
```

---

### **SPÔSOB 2: Manuálne príkazy**

#### Krok 1: Klonujte repo (ak ešte nemáte)
```bash
git clone https://github.com/tnagy421/cf-forecast.git
cd cf-forecast
```

#### Krok 2: Skopírujte aplikačné súbory

Stiahnite tieto súbory z nášho balíka a vložte ich do `cf-forecast` zložky:
- `app.py`
- `cf_predictor.py`
- `requirements.txt`
- `README.md`
- `QUICK_START_GUIDE.md`
- `TESTING_PLAN.md`

#### Krok 3: Git commit a push
```bash
# Nakonfigurujte Git (prvýkrát)
git config --global user.name "Vaše Meno"
git config --global user.email "vasa.email@gmail.com"

# Pridajte súbory
git add .

# Vytvorte commit
git commit -m "Add CF Forecast WebApp"

# Pushnte na GitHub
git push -u origin main
```

**Keď Git spýta na heslo:**
- Username: `tnagy421`
- Password: Použite GitHub Personal Access Token (nie heslo!)
  - V GitHub: Settings → Developer settings → Personal access tokens → Tokens (classic)
  - Scope: `repo` + `workflow`

---

## 🌐 Krok 3: Deployujte na Streamlit Cloud

### 1. Vytvorte Streamlit Cloud konto

Choďte na: https://streamlit.io/cloud

Kliknite "Sign up with GitHub" (používajte váš GitHub účet `tnagy421`)

### 2. Autorizujte GitHub

Streamlit Cloud vás požiada o povolenie prístupu k vašim repom. Kliknite "Authorize".

### 3. Deployujte aplikáciu

Na https://streamlit.io/cloud kliknite **"New app"**

Vyplňte:
- **Repository**: `tnagy421/cf-forecast`
- **Branch**: `main`
- **Main file path**: `app.py`

Kliknite **"Deploy"**

### 4. Čakajte

Streamlit Cloud:
1. Stiahne váš kód z GitHub
2. Nainštaluje Python balíčky (z `requirements.txt`)
3. Spustí `app.py`
4. Vytvorí verejný URL

**Trvá 1-3 minúty.** Počkajte na "App is running" správu.

---

## ✅ Výsledok

Vaša aplikácia bude dostupná na:

```
https://cf-forecast-XXXXX.streamlit.app
```

URL si zapamätajte a zdieľajte s tímom! 🎉

---

## 🔄 Ďalšie updaty

Keď budete chcieť aplikáciu upraviť:

1. Upravte kód lokálne (`app.py`, `cf_predictor.py`, atď.)
2. Pushnte zmeny na GitHub:
   ```bash
   git add .
   git commit -m "Update: [čo ste zmenili]"
   git push
   ```
3. Streamlit Cloud **automaticky** nasadí novú verziu! 🚀

---

## 🆘 Riešenie problémov

### ❌ "fatal: not a git repository"
```bash
cd cf-forecast
```
Uistite sa, že ste v správnej zložke.

### ❌ "Permission denied" pri git push
```bash
# Skontrolujte, že používate token, nie heslo
# Token by mal začínať: github_pat_...
```

### ❌ "Repository not found"
- Uistite sa, že repo je **Public** (nie Private)
- GitHub → Settings → Repository visibility → Public

### ❌ "App deployment failed" na Streamlit Cloud
Skontrolujte logs:
1. Streamlit Cloud → Your app → Settings
2. Pozrite "View logs"
3. Hľadajte chyby (zvyčajne chýba balíček v `requirements.txt`)

---

## 📱 Keď funguje:

✅ Aplikácia beží na Streamlit Cloud  
✅ Bez Pythonu na vašom počítači  
✅ Všetci sa logia cez web URL  
✅ Automatické updaty z GitHub  
✅ Bezplatné (free tier)  

---

## 🎓 Streamlit Cloud Features

| Funkcia | Dostupné? |
|---------|-----------|
| Public URL | ✅ Áno |
| HTTPS | ✅ Áno |
| Custom domain | ❌ Nie (free tier) |
| Secrets management | ✅ Áno |
| Email alerts | ✅ Áno |

---

## 📞 Ďalšia pomoc

- **Streamlit dokumentácia**: https://docs.streamlit.io/deploy/streamlit-cloud
- **GitHub Help**: https://docs.github.com
- **Problémy s aplikáciou**: Skontrolujte `QUICK_START_GUIDE.md`

---

**Hotovo?** Gratulujem! 🎉 Vaša aplikácia je na webe! 🚀
