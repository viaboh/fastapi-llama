## Setup Instructions
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the FastAPI server:
   ```bash
   uvicorn app:app --reload
   ```
3. Test API with a POST request to:
   ```http
   http://127.0.0.1:8000/generate_tasks
   ```
   Example JSON body:
   ```json
   {
     "user_input": "Send two extra pillows and clean my room"
   }