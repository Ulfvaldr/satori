# Setting Up a Python Environment for ML, AI, Data Science, and API Development on Ubuntu

## Step 1: Install Python
Ensure Python 3 is installed:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

## Step 2: Set Up a Virtual Environment
Create an isolated environment to manage dependencies:

```bash
python3 -m venv ml_env
source ml_env/bin/activate
```

## Step 3: Upgrade pip
Upgrade pip to the latest version:

```bash
pip install --upgrade pip
```

## Step 4: Install Key Python Libraries
Install commonly used libraries for ML, AI, Data Science, and API development:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn scipy --break-system-packages
pip install tensorflow keras pytorch torchvision --break-system-packages
pip install jupyter jupyterlab notebook --break-system-packages
pip install flask fastapi uvicorn --break-system-packages
pip install requests beautifulsoup4 --break-system-packages
pip install plotly dash bokeh --break-system-packages
pip install sqlalchemy pymongo --break-system-packages
pip install opencv-python pillow --break-system-packages
pip install nltk spacy --break-system-packages
pip install gensim transformers --break-system-packages
pip install gunicorn httpx --break-system-packages
pip install pytest black flake8 --break-system-packages
pip install pandas-profiling --break-system-packages
pip install xgboost lightgbm catboost --break-system-packages
```

## Step 5: Install Additional Tools

### Jupyter Notebook Extensions:
```bash
pip install jupyter_contrib_nbextensions --break-system-packages
jupyter contrib nbextension install --user
```

### Visualization Libraries:
```bash
pip install folium geopandas --break-system-packages
```

### Deep Learning Frameworks (Optional):
```bash
pip install mxnet --break-system-packages
```

### AutoML Libraries:
```bash
pip install h2o pycaret --break-system-packages
```

## Step 6: Test the Environment
Test that key libraries are installed and working:

```bash
python -c "import numpy, pandas, tensorflow, flask, fastapi; print('Environment ready!')"
```

## Step 7: Deactivate the Virtual Environment
When done, deactivate the virtual environment:

```bash
deactivate
```

## Step 8: Optional - Save and Reuse Requirements
To save installed libraries for reuse:

```bash
pip freeze > requirements.txt
```



## Steps to Install with --break-system-packages:
Save the above file as requirements.txt in your project's root directory.

Use the following command to install all the packages:

```bash
pip install -r requirements.txt --break-system-packages
```
This will ensure all the specified packages are installed in your environment with the required permission bypass. Let me know if you need further help!







