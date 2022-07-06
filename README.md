# DruidDetector
DruidDetector is a web framework (Flask-based) that takes Android APK file and analyze it to extract features (permission-based, gray-image based) using static analysis and pass them to multiple ensembled deep learning models for apk malware detection


## To run the framework what you need is:
- Having python3.
- Install [Anaconda3](https://www.anaconda.com/products/distribution)
- Create virtual environment using conda
```
conda create --name <environment-name> python==3.8
conda activate <environment-name>
```
- Install the requirements within conda environment using ```pip install -r requirements.txt```.
- [Download](https://mega.nz/file/jVhEUKYC#bz1053qWtBb1TGyippIPHIiN94BJKWTnzvzwGHr3xxY) and extract the pre-trained models on the main folder.
- Import the db.sql file into the mysql via CLI or phpmyadmin
- Modify Lines 18-21 in app.py file based on your mysql information
- Run: ```python3 app.py```



## Result
Our framework reached 94.81% accuracy in dex-based CNN model, also reached 97.02% accuracy in permission-based CNN model
<img src="https://user-images.githubusercontent.com/63113401/177514576-9bc6d066-8cd6-4cd2-8ac9-e53febdc2c06.png" width="300" height="300" />


if you noticed any mistake or have any suggestion reach us at LinkedIn:

[![Mohamad Albawab](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mhmdba/) Mohamad Albawab

[![Mohamad Kontar](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mhmdqi/) Mohamad Kontar


