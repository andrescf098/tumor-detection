# tumor-detection

### Virtual enviroment

Use the command **"python -m venv env"** for to create the virtual enviroment and then,

Active the virtual enviroment with the command **".\env\Scripts\activate"** in the folder of the project

### Required modules

Now use the **"pip freeze -r requirements.txt"** for download the required modules

### Dataset

https://www.kaggle.com/datasets/adityakomaravolu/brain-tumor-mri-images

Put the dataset in **"app/files"**

### Model training

Use the command **"python train_model.py"**, this will take several minutes and depends on whether or not a GPU is used.

### Backend

Use the command **"uvicorn app.main:app --reload"** for the run of server
