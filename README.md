# Overview

# To add new 3GPP specification Documents
- Extract (copy) the text of the desired document, open the "3GPP_raw_text.txt" file and add by pasting
# To Run
- Install the required dependencies by running the command "pip install -r requirements.txt"
- Go to the files 'qdrant.py' and 'answer.py' and replace the placeholders with your actual API key.
- Start qdrant by running the command 'docker run -p 6333:6333 qdrant/qdrant'
- Navigate into the main project folder "nugt",run the file 'qdrant.py' using the command 'python qdrant.py' to index files to qdrant.
- From the repo root, start the server by running python mysite/manage.py runserver
- Access site at the url on the terminal. The default is http://127.0.0.1:8000/
- Access the NGT chatbot by running the command "http://127.0.0.1:8000/nugt/chat/"
