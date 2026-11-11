# CLAUDE.md — florence-labeling

Document de reprise à froid. Rédigé le 2026-11-11 après exploration du dépôt (code, historique, .gitignore, venv local).

## 1. Objectif et contexte

- Petit outil **CLI** qui étiquette automatiquement un dossier d'images avec le modèle vision-langage **Microsoft Florence-2** (`microsoft/Florence-2-base`, Hugging Face) et exporte les résultats en **CSV**.
- Trois modes : détection d'objets (liste des classes trouvées), description courte, description détaillée.
- Usage personnel / expérimental (constitution de jeux de données étiquetés). Exemples locaux : photos de chanteurs (dossiers `images/jony`, `images/patoche`).
- Dépôt : `https://github.com/Tarekivida/florence-labeling.git`. Un seul fichier de code (`main.py`, ~100 lignes).

## 2. Stack et versions

- Python ≥ 3.9 (README) ; venv local en **Python 3.13**. Testé sur macOS Apple Silicon (README).
- Versions installées dans le venv local (juillet 2025) : `torch 2.7.1`, `torchvision 0.22.1`, `transformers 4.53.2`, `timm 1.0.17`, `einops 0.8.1`, `huggingface_hub 0.33.4`, `tokenizers 0.21.2`, `numpy 2.2.6`, Pillow.
- `requirements.txt` est **non épinglé** (noms seuls). La version épinglée exacte existe dans l'historique : `git show 3a8b76f:requirements.txt` (versions ci-dessus).
- Florence-2 nécessite `trust_remote_code=True` (code modèle téléchargé depuis le Hub) ; `einops` et `timm` sont requis par ce code distant. `opencv-python` est listé mais non importé.

## 3. Arborescence

```
florence-labeling/
├── main.py              # Tout le code : chargement modèle, choix du mode, parcours récursif, écriture CSV
├── requirements.txt     # Dépendances (non épinglées)
├── README.md            # Mode d'emploi (anglais)
├── images/              # Images d'exemple (suivies par git) : jony/ (1 jpg), patoche/ (2 images)
├── labels/              # Sorties CSV ; OD_images.csv suivi par git (sauvegarde du 2026-11-11)
└── .gitignore
```

Hors git : `venv/`, `__pycache__/`, `labels.csv`, `.DS_Store`.

## 4. Fonctionnement (main.py)

1. **À l'import** (niveau module) : choix du device (`cuda` sinon `cpu`, fp16 sur CUDA, fp32 sinon), chargement du modèle et du processeur Florence-2-base, puis `choose_prompt()` (saisie clavier 1/2/3).
   - 1 → `<OD>` (détection d'objets) ; 2 → `<DETAILED_CAPTION>` ; 3 → `<MORE_DETAILED_CAPTION>` ; autre → `<DETAILED_CAPTION>`.
2. `main()` : vérifie l'argument (dossier), crée `labels/`, nomme la sortie `labels/<OD|DETAILED|MORE_DETAILED>_<nom_du_dossier>.csv`.
3. `os.walk` récursif ; extensions `.jpg`, `.jpeg`, `.png`.
4. `process_image` : `generate(max_new_tokens=512, num_beams=3)`. En mode `<OD>`, les noms de classes sont extraits par regex `([a-zA-Z ]+)<loc_\d+>` du texte brut, dédupliqués et triés (les boîtes englobantes sont **jetées**). Sinon, décodage simple.
5. CSV : colonnes `file_path, file_name, label`. Erreurs par image affichées et ignorées.

## 5. Installation et lancement

```bash
git clone https://github.com/Tarekivida/florence-labeling.git && cd florence-labeling
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt        # ou, pour les versions éprouvées : git show 3a8b76f:requirements.txt > req.lock && pip install -r req.lock
python main.py images                  # puis choisir 1, 2 ou 3
# → labels/OD_images.csv (si mode 1)
```

- Premier lancement : téléchargement de `microsoft/Florence-2-base` (~0,5 Go) dans `~/.cache/huggingface/hub` (localement, Florence-2-base **et** Florence-2-large y sont présents).
- Pas de tests, pas de build, pas de CI, pas de déploiement.

## 6. Variables d'environnement et services externes

- Aucune variable requise. Le modèle est public : pas besoin de token Hugging Face. Optionnel : `HF_TOKEN` (limites de débit Hub) ou `HF_HOME` (emplacement du cache), variables standard de `huggingface_hub`, non utilisées explicitement par le code.
- Service externe : Hugging Face Hub (téléchargement du modèle et de son code distant au premier lancement).

## 7. Données hors git

- `venv/` : à recréer.
- Cache du modèle (`~/.cache/huggingface`) : hors du repo, re-téléchargé automatiquement.
- `labels.csv` (ancien nom de sortie unique) est ignoré ; les CSV dans `labels/` ne le sont pas réellement (voir piège `.gitignore`).
- Les images d'exemple sont dans git (≈156 Ko) ; ce sont des photos de presse de personnalités (droits d'auteur probablement non libres — à ne pas redistribuer largement).

## 8. État, TODO, bugs connus

État : fonctionnel, petit outil terminé (dernier développement juillet 2025).

Points faibles constatés :
- **Pas de support MPS** (GPU Apple Silicon) : sur Mac, tourne en CPU fp32 (lent). Ajouter `torch.backends.mps.is_available()`.
- Le modèle se charge et la question du mode est posée **avant** la vérification des arguments : `python main.py` sans argument charge le modèle et demande le mode avant d'afficher l'usage.
- Libellés incohérents : le menu dit « 1. Object Description » / « 2. Light Description » alors que le README parle d'« Object Detection » ; « Light » utilise `<DETAILED_CAPTION>` (Florence a aussi `<CAPTION>`, plus court, non proposé).
- En mode OD, la regex ne garde que les lettres/espaces : les étiquettes avec chiffres, tirets ou accents sont tronquées ; les coordonnées sont perdues.
- Un fichier CSV existant du même nom est **écrasé** sans avertissement.
- Extensions limitées (pas de `.webp`, `.heic`, `.bmp`).
- `requirements.txt` non épinglé : une version récente de `transformers` peut casser le code distant de Florence-2 (problème connu de compatibilité) → préférer les versions de `3a8b76f`.
- `opencv-python` inutile.

## 9. Conventions et pièges

- **`.gitignore`** : la ligne `.DS_Storelabels/` est une concaténation accidentelle de `.DS_Store` et `labels/`. Intention initiale probable : ignorer `labels/`. Actuellement `labels/` n'est pas ignoré et `labels/OD_images.csv` est volontairement suivi (commit de sauvegarde).
- Les chemins dans le CSV sont relatifs au répertoire de lancement (tels que passés en argument).
- Exécuter depuis la racine du repo (la sortie `labels/` est relative au cwd).

## 10. Reprendre le projet

1. Cloner, créer `venv`, installer les versions épinglées de `3a8b76f`.
2. `python main.py images` → mode 1 → comparer avec `labels/OD_images.csv` (résultat de référence : « guitar, human face, person », etc.).
3. Améliorations rapides : support MPS, parsing des arguments (argparse : dossier, mode, modèle base/large, fichier de sortie) avant le chargement du modèle, conservation des bounding boxes en mode OD (via `processor.post_process_generation`), correction du `.gitignore`.
