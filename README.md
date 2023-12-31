## Document based Chatbot

**Python Version Used: 3.11.3**

Steps to run on your PC/ Local Machine: -

1. Open Terminal, got to any directory of your choice and clone this repo. 

   ```
   git clone https://github.com/ramankumar-1/docbot.git
   ```

3. Download all the required Python packages.

   ```
   pip install -r requirements.txt
   ```

5. Create an environment file (.env) for storing the API keys. 

   ```
   touch .env
   ```

7. Create Account and obtain your [Huggingface](https://huggingface.co/settings/tokens) and [Cohere](https://dashboard.cohere.com/api-keys) API keys. 
8. Add the API keys to the Environment Variable File (.env) which you just created.<br>
	```
	HUGGINGFACEHUB_API_TOKEN=<your-hugging-face-api-key>
	COHERE_API_KEY=<your-cohere-api-key>
	```
9. Run the application. 

    ```
   streamlit run app.py
    ```
