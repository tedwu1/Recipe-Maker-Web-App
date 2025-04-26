# Recipe Maker Web App
- Theodore Wu (@tedwu1)
- Natalie Tran (@nataliehtran)
- Hari Kotamsetti (@AwesomenessReborn)

## Application Development Setup

First, get the project locally using git provider. 

You can use either conda or venv for package managment, both reflect the dependencies invovled using project. Conda environment is recommended. 

### Using Conda
```
conda env create -f environment.yml
conda activate recipe-app
```

### Using venv
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the App

```
flask --app app run
```